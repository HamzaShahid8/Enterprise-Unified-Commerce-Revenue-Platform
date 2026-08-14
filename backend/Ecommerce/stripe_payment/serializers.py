from rest_framework import serializers
from rest_framework import serializers
from .models import Payment


class PaymentReadSerializer(serializers.ModelSerializer):
    order_code = serializers.CharField(source='order.code', read_only=True)
    
    class Meta:
        model = Payment

        fields = [
            "id",
            "order_code",
            "provider",
            "payment_intent_id",
            "amount",
            "currency",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields


class PaymentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment

        fields = [
            "order",
        ]


class CreatePaymentIntentSerializer(serializers.Serializer):
    order_code = serializers.CharField()