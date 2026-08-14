from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from .services import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from monitoring.models import ActivityLogs
from monitoring.utils import create_log

# Create your views here.

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    permission_classes = [HasPermission, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PermissionsReadSerializer
        return PermissionsWriteSerializer
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_permission'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_permission'
            
        elif self.action in ['partial_update', 'update']:
            permission.required_permission = 'update_permission'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_permission'
            
        return [IsAuthenticated(), permission]
    
    def perform_create(self, serializer):
        
        permission = serializer.save()
        
        create_log(
            user=self.request.user,
            action='create',
            model_name='Permissions',
            object_id=permission.id,
            description=(
                f"Permission name: {permission.name}"
                f"Create by: {self.request.user.username}."
            )
        )
        
    def perform_update(self, serializer):
        
        permission = serializer.save()
        
        create_log(
            user=self.request.user,
            action='update',
            model_name='Permissions',
            object_id=permission.id,
            description=(
                f"Permission name: {permission.name}"
                f"Updated by: {self.request.user.username}."
            )
        )
        
    def perform_destroy(self, instance):
        
        permission_id = instance.id
        permission_name = instance.name
        
        create_log(
            user=self.request.user,
            action='delete',
            model_name='Permissions',
            object_id=permission_id,
            description=(
                f"Permission name: {permission_name}"
                f"Deleted by: {self.request.user.username}"
            )
        )
        
        instance.delete()
    
class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [HasPermission, IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RolesReadSerializer
        return RolesWriteSerializer
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_role'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_role'
            
        elif self.action in ['partial_update', 'update']:
            permission.required_permission = 'update_role'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_role'
            
        return [IsAuthenticated(), permission]
    
    def perform_create(self, serializer):
        
        role = serializer.save()
        
        create_log(
            user=self.request.user,
            action='create',
            model_name='Roles',
            object_id=role.id,
            description=(
                f"Role name: {role.name}"
                f"Create by: {self.request.user.username}."
            )
        )
        
    def perform_update(self, serializer):
        
        role = serializer.save()
        
        create_log(
            user=self.request.user,
            action='update',
            model_name='Role',
            object_id=role.id,
            description=(
                f"Role name: {role.name}"
                f"Updated by: {self.request.user.username}."
            )
        )
        
    def perform_destroy(self, instance):
        
        role_id = instance.id
        role_name = instance.name
        
        create_log(
            user=self.request.user,
            action='delete',
            model_name='Roles',
            object_id=role_id,
            description=(
                f"Role name: {role_name}"
                f"Deleted by: {self.request.user.username}"
            )
        )
        
        instance.delete()