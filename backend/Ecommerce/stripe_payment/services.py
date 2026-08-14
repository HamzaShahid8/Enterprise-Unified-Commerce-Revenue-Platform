from decimal import Decimal
import stripe
from django.conf import settings
from django.db import transaction
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:

    @staticmethod
    @transaction.atomic
    def create_payment_intent(order):
        amount = int(order.total_amount * Decimal("100"))
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={
                'enabled': True
            },
            metadata={
                'order_code': str(order.code)
            }
        )
        payment = Payment.objects.create(
            order=order,
            provider='stripe',
            payment_intent_id=payment_intent.id,
            amount=order.total_amount,
            currency='usd',
            status='pending'
        )
        
        return payment, payment_intent