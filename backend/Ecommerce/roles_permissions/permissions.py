from rest_framework.permissions import BasePermission
from roles_permissions.models import *
from .services import has_permission

class HasPermission(BasePermission):
    
    required_permission = None
    
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False
        
        if not self.required_permission:
            return True
        
        return has_permission(request.user, self.required_permission)