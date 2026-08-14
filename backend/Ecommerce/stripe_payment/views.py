from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.models import Order
from .serializers import CreatePaymentIntentSerializer
from .services import PaymentService
import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Payment
from roles_permissions.models import *
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework import viewsets
from .serializers import *

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    queryset = Payment.objects.select_related('order', 'order__user')
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PaymentReadSerializer
        return PaymentWriteSerializer


    def get_permissions(self):

        permission = HasPermission()

        if self.action == "create":
            permission.required_permission = "create_payment"

        elif self.action in ["list", "retrieve"]:
            permission.required_permission = "view_payment"

        elif self.action == "cancel":
            permission.required_permission = "cancel_payment"

        return [
            IsAuthenticated(),
            permission,
        ]


class CreatePaymentIntentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CreatePaymentIntentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        order_code = serializer.validated_data["order_code"]

        order = get_object_or_404(
            Order,
            code=order_code,
            user=request.user
        )

        payment, payment_intent = (
            PaymentService.create_payment_intent(order)
        )
        
        create_log(
            user=request.user,
            action="payment",
            model_name="Payment",
            object_id=payment.id,
            description=(
                f"Payment intent created for "
                f"Order {order.code}."
            )
        )
        
        response_serializer = PaymentReadSerializer(
            payment
        )

        return Response(
            {
                "payment": response_serializer.data,
                "client_secret": payment_intent.client_secret,
            },
            status=status.HTTP_201_CREATED,
        )


class StripeWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        payload = request.body

        signature = request.META.get(
            "HTTP_STRIPE_SIGNATURE"
        )

        # Verify Stripe webhook
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
            )

        except ValueError:
            return HttpResponse(
                "Invalid payload",
                status=400,
            )

        except stripe.error.SignatureVerificationError:
            return HttpResponse(
                "Invalid signature",
                status=400,
            )

        event_type = event["type"]

        payment_intent = event["data"]["object"]

        payment_intent_id = payment_intent["id"]

        # PAYMENT SUCCESSFUL
        if event_type == "payment_intent.succeeded":

            with transaction.atomic():

                payment = (
                    Payment.objects
                    .select_for_update()
                    .select_related("order")
                    .get(
                        payment_intent_id=payment_intent_id
                    )
                )

                # Prevent duplicate processing
                if payment.status != Payment.Status.SUCCEEDED:

                    payment.status = (
                        Payment.Status.SUCCEEDED
                    )

                    payment.save(
                        update_fields=[
                            "status",
                            "updated_at",
                        ]
                    )

                    # Mark order as paid
                    order = payment.order

                    order.status = "paid"

                    order.save(
                        update_fields=[
                            "status",
                        ]
                    )

        # PAYMENT FAILED
        elif event_type == "payment_intent.payment_failed":

            with transaction.atomic():

                payment = (
                    Payment.objects
                    .select_for_update()
                    .get(
                        payment_intent_id=payment_intent_id
                    )
                )

                # Prevent duplicate processing
                if payment.status != Payment.Status.FAILED:

                    payment.status = (
                        Payment.Status.FAILED
                    )

                    payment.save(
                        update_fields=[
                            "status",
                            "updated_at",
                        ]
                    )

        # PAYMENT CANCELED
        elif event_type == "payment_intent.canceled":

            with transaction.atomic():

                payment = (
                    Payment.objects
                    .select_for_update()
                    .get(
                        payment_intent_id=payment_intent_id
                    )
                )

                # Prevent duplicate processing
                if payment.status != Payment.Status.CANCELED:

                    payment.status = (
                        Payment.Status.CANCELED
                    )

                    payment.save(
                        update_fields=[
                            "status",
                            "updated_at",
                        ]
                    )

        return HttpResponse(
            "Webhook received",
            status=200,
        )