from django.shortcuts import render
from .services import *
from .models import *
from .serializers import *
from roles_permissions import models
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from monitoring.models import ActivityLogs
from monitoring.utils import create_log

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('order_items__product__product')
    permission_classes = [IsAuthenticated, HasPermission]
    
    lookup_field = 'code'
    
    def get_serializer_class(self):
        if self.action in ['list',  'retrieve']:
            return OrderReadSerializer
        return OrderWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name in ['manager', 'employe']:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        if self.request.user.role.name in ['manager', 'employe']:
            serializer.save()
            
        else:
            serializer.save(user = self.request.user)
            
    def create(self, request, *args, **kwargs):
        
        idempotency_key = request.headers.get('idempotency_key')
        
        if not idempotency_key:
            return Response({
                'detail': 'Idempotency-Key header is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = OrderWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        response_data, status_code = OrderService.create_order(serializer.validated_data, request.user, idempotency_key=idempotency_key)
        
        create_log(
            user=request.user,
            action='create',
            model_name='Order',
            object_id=response_data.get('id'),
            description='Order created successfully.'
        )
            
        return Response(
            response_data,
            status = status_code
        )
            
    def perform_update(self, serializer):
        order = OrderService.update_order(order=serializer.instance, validated_data=serializer.validated_data)
        
        create_log(
            user=self.request.user,
            action='update',
            model_name='Order',
            object_id=order.id,
            description='Order updated successfully.'
        )
            
    def perform_destroy(self, instance):
        create_log(
            user=self.request.user,
            action='delete',
            model_name='Order',
            object_id=instance.id,
            description='Order deleted successfully.'
        )
        OrderService.delete_order(order=instance)
        
    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)

        create_log(
            user=request.user,
            action='view',
            model_name='Order',
            escription='Order list viewed.'
        )

        return response
    
    def retrieve(self, request, *args, **kwargs):

        response = super().retrieve(request, *args, **kwargs)

        create_log(
            user=request.user,
            action='view',
            model_name='Order',
            object_id=str(self.get_object().id),
            description='Order viewed successfully.'
        )

        return response
            
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_order'
            
        elif self.action == 'create':
            permission.required_permission = 'create_order'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_order'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_permission'
            
        return [IsAuthenticated(), permission]
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order__user', 'product')
    permission_classes = [IsAuthenticated, HasPermission]
    
    lookup_field = 'code'
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderItemReadSerializer
        return OrderItemWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name in ['manager', 'employe']:
            return OrderItem.objects.all()
        else:
            return OrderItem.objects.all()
        
    def perform_create(self, serializer):

        order_item = serializer.save()

        create_log(
            user=self.request.user,
            action='create',
            model_name='OrderItem',
            object_id=order_item.id,
            description=(
                f"Order item for Order "
                f"{order_item.order.code} created successfully."
            )
        )
        
    def perform_update(self, serializer):

        order_item = serializer.save()

        create_log(
            user=self.request.user,
            action='update',
            model_name='OrderItem',
            object_id=order_item.id,
            description=(
                f"Order item for Order "
                f"{order_item.order.code} updated successfully."
            )
        )
        
    def perform_destroy(self, instance):

        order_item_id = instance.id
        order_code = instance.order.code

        create_log(
            user=self.request.user,
            action='delete',
            model_name='OrderItem',
            object_id=order_item_id,
            description=(
                f"Order item from Order "
                f"{order_code} deleted successfully."
            )
        )

        instance.delete()
        
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_order_item'
        
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_order_item'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_order_item'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_order_item'
            
        return [IsAuthenticated(), permission]