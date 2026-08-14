from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem, IdempotancyKey
from products.models import Product
from .serializers import *
from billing.models import Invoice
from billing.services import *

class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(validated_data, user, idempotency_key):
        
        # check existing
        existing = IdempotancyKey.objects.filter(
            key=idempotency_key,
            user=user
        ).first()
        
        if existing:
            return existing.response_data, existing.status_code

        items = validated_data.pop("items", [])

        order = Order.objects.create(
            user=user,
            **validated_data
        )

        for item in items:

            variant = item["product"]

            product = (
                Product.objects
                .select_for_update()
                .get(pk=variant.product_id)
            )

            quantity = item["quantity"]

            if product.stock < quantity:
                raise ValidationError("Out of stock")

            OrderItem.objects.create(
                order=order,
                product=variant,
                quantity=quantity,
                price=variant.price
            )

            product.stock -= quantity
            product.save(update_fields=["stock"])

        order.calculate_total()
        
        InvoiceService.create_invoice(order)
        
        # Prepare response
        response_data = OrderReadSerializer(order).data
        
        IdempotancyKey.objects.create(
            key=idempotency_key,
            user=user,
            response_data=response_data,
            status_code=201
        )
        return response_data, 201


    @staticmethod
    @transaction.atomic
    def update_order(order, validated_data):

        items = validated_data.pop("items", None)

        # Order ke normal fields update
        for field, value in validated_data.items():
            setattr(order, field, value)

        order.save()

        # Agar items update nahi aaye
        if items is None:
            return order

        # Existing items delete + stock restore
        old_items = list(
            order.order_items.select_related("product__product")
        )

        for old_item in old_items:

            product = (
                Product.objects
                .select_for_update()
                .get(pk=old_item.product.product_id)
            )

            product.stock += old_item.quantity
            product.save(update_fields=["stock"])

        order.order_items.all().delete()

        # New items create
        for item in items:

            variant = item["product"]

            product = (
                Product.objects
                .select_for_update()
                .get(pk=variant.product_id)
            )

            quantity = item["quantity"]

            if product.stock < quantity:
                raise ValidationError(
                    f"Out of stock for {variant.product.name}"
                )

            OrderItem.objects.create(
                order=order,
                product=variant,
                quantity=quantity,
                price=variant.price
            )

            product.stock -= quantity
            product.save(update_fields=["stock"])

        order.calculate_total()

        return order


    @staticmethod
    @transaction.atomic
    def delete_order(order):

        # Restore stock before deleting items
        old_items = list(
            order.order_items.select_related("product__product")
        )

        for item in old_items:

            product = (
                Product.objects
                .select_for_update()
                .get(pk=item.product.product_id)
            )

            product.stock += item.quantity
            product.save(update_fields=["stock"])

        # OrderItem CASCADE se automatically delete honge
        order.delete()