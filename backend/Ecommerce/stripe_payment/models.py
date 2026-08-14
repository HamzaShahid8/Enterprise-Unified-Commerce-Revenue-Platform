from django.db import models
from profiles.models import UUID
from accounts.models import BaseModel



class Payment(BaseModel, UUID):
    
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payment_order",
        null=True,
        blank=True
    )

    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='stripe', null=True, blank=True)

    payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=3,
        default="usd",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending',
        null=True,
        blank=True
    )