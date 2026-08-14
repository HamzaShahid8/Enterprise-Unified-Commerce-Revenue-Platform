from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .services import *
from .models import Invoice
from .serializers import InvoiceSerializer
from roles_permissions.models import Roles, Permissions
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from monitoring.models import ActivityLogs
from monitoring.utils import create_log

# Create your views here.

class InvoiceViewSet(ModelViewSet):
    
    queryset = Invoice.objects.select_related('order', 'order__user')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    
    lookup_field = 'code'
    
    http_method_names = ['get', 'put', 'patch', 'delete']
    
    def perform_update(self, serializer):
        invoice = InvoiceService.update_invoice(
            invoice=self.get_object(),
            validated_data=serializer.validated_data
        )
        
        create_log(
            user=self.request.user,
            action='update',
            model_name='Invoice',
            object_id=invoice.id,
            description=(
                f"Invoice {invoice.code} "
                f"updated successfully."
            )
        )
        
    def perform_destroy(self, instance):

        invoice_id = instance.id
        invoice_code = instance.code

        create_log(
            user=self.request.user,
            action='delete',
            model_name='Invoice',
            object_id=invoice_id,
            description=(
                f"Invoice {invoice_code} "
                f"deleted successfully."
            )
        )

        InvoiceService.delete_invoice(instance)
        
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name in ['manager', 'employe']:
            return Invoice.objects.select_related('order', 'order__user').all()
        
        return Invoice.objects.select_related('order', 'order__user').filter(order__user=user)
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_bill'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_bill'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_bill'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_bill'
            
        return [IsAuthenticated(), permission]