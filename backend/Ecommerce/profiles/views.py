from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from roles_permissions.models import Roles
from monitoring.models import ActivityLogs
from monitoring.utils import create_log

# Create your views here.


class CustomerProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomerProfileReadSerializer
        return CustomerProfileWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name in ['manager', 'employe']:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name == 'manager':
            customer = serializer.save()
        else:
            customer = serializer.save(user=user)
            
        create_log(
            user=user,
            action='create',
            model_name='CustomerProfile',
            object_id=customer.id,
            description='Customer profile created'
        )
        
        def perform_update(self, serializer):
        
            customer = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='CustomerProfile',
                object_id=customer.id,
                description='Customer profiles updated'
            )
            
        def perform_destroy(self, instance):
        
            customer_id = instance.id
            customer_name = instance.name
        
            create_log(
                user=self.request.user,
                action='delete',
                model_name='CustomerProfile',
                object_id=customer_id,
                description='Customer profile deleted'
            )
        
            instance.delete()
        
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_customer_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_customer_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_customer_profile'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_customer_profile'
            
        return [IsAuthenticated(), permission]
    
class ManagerProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ManagerProfileReadSerializer
        return ManagerProfileWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name == 'manager':
            return ManagerProfile.objects.filter(user=user)
    
    def perform_create(self, serializer):
            manager = serializer.save(user=self.request.user)
            
            create_log(
                user=self.request.user,
                action='create',
                model_name='ManagerProfile',
                object_id=manager.id,
                description=f"Manager profile created"
            )
            
    def perform_update(self, serializer):
        
            manager = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='ManagerProfile',
                object_id=manager.id,
                description='Manager profiles updated'
            )
            
    def perform_destroy(self, instance):
        
        manager_id = instance.id
        
        create_log(
            user=self.request.user,
            action='delete',
            model_name='ManagerProfile',
            object_id=manager_id,
            description='Manager profile deleted'
        )
        
        instance.delete()
        
            
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_manager_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_manager_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_manager_profile'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_manager_profile'
            
        return [IsAuthenticated(), permission]
    
class EmployeeProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EmployeeProfileReadSerializer
        return EmployeeProfileWriteSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role.name == 'manager':
            return EmployeeProfile.objects.all()
        return EmployeeProfile.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role.name == 'manager':
            employe = serializer.save()
        else:
            employe = serializer.save(user=user)
            
        create_log(
            user=self.request.user,
            action='create',
            model_name='EmployeeProfile',
            object_id=employe.id,
            description='Employe profile created'
        )
        
    def perform_update(self, serializer):
        
            employe = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='EmployeeProfile',
                object_id=employe.id,
                description='Employe profile updated'
            )
            
    def perform_destroy(self, instance):
        
        employe_id = instance.id
        
        create_log(
            user=self.request.user,
            action='delete',
            model_name='EmployeeProfile',
            object_id=employe_id,
            description='Employe profile deleted'
        )
        
        instance.delete()
            
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_employee_profile'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_employee_profile'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_employee_profile'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_employee_profile'
            
        return [IsAuthenticated(), permission]