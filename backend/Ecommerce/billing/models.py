from decimal import Decimal
from django.db import models
from accounts.models import BaseModel
from profiles.models import UUID


class Invoice(BaseModel, UUID):

    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='invoice'
    )

    subtotal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00")
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.CharField(
        max_length=30,
        default="unpaid"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Invoice - {self.order.code}"