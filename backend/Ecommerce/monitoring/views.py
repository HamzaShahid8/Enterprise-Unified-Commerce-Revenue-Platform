from django.shortcuts import render
from .serializers import ActivityLogReadSerializer, ActivityLogWriteSerializer
from .models import ActivityLogs
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from roles_permissions.models import *
from roles_permissions.permissions import *
from roles_permissions.services import *

# Create your views here.

class ActivityLogsViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ActivityLogReadSerializer
        return ActivityLogWriteSerializer
    
    def get_queryset(self):
        
        user = self.request.user
        
        if user.role.name in ['manager', 'employe']:
            return ActivityLogs.objects.all()
        else:
            return ActivityLogs.objects.filter(user=user)
        
    def perform_create(self, serializer):
        serializer.save()
        
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_activity_logs'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_activity_logs'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_activity_logs'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_activity_logs'
            
        return [IsAuthenticated(), permission]