from django.db.models import Sum
from decimal import Decimal
from .models import Invoice
from django.db import transaction

class InvoiceService:
    
    @staticmethod
    @transaction.atomic
    def create_invoice(order):
        subtotal = (
            order.order_items.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
        )
        
        tax = order.tax or Decimal('0.00')
        shipping = order.shipping_cost or Decimal('0.00')
        discount = order.discount or Decimal('0.00')
        
        total_amount = (
            subtotal + tax + shipping - discount
        )
        
        invoice = Invoice.objects.create(
            order=order,
            subtotal=subtotal,
            tax=tax,
            shipping_cost=shipping,
            discount=discount,
            total_amount=total_amount
        )
        
        return invoice
    
    @staticmethod
    @transaction.atomic
    def update_invoice(invoice, validated_data):

        for field, value in validated_data.items():
            setattr(invoice, field, value)

        invoice.save()

        return invoice

    @staticmethod
    @transaction.atomic
    def delete_invoice(invoice):

        invoice.delete()
        
        return True