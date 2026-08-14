from rest_framework import serializers
from .models import Order, OrderItem
from products.models import *

class OrderItemReadSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['code', 'product', 'quantity', 'price', 'subtotal', 'created_at', 'updated_at']
        
class OrderReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    items = OrderItemReadSerializer(many=True, read_only=True, source='order_items')
    
    class Meta:
        model = Order
        fields = ['code', 'user', 'status', 'payment_status', 'tax', 'shipping_cost', 'discount', 'shipping_address', 'total_amount', 'subtotal', 'created_at', 'updated_at', 'items']
        
class OrderItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset = ProductVariant.objects.all(), slug_field='code')
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        
class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'items']