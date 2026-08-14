from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    order = serializers.CharField(source='order.code', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            "code",
            "order",
            "subtotal",
            "tax",
            "shipping_cost",
            "discount",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = fields