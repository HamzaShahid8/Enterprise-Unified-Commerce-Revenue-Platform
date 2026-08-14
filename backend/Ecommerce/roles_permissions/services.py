from roles_permissions.models import *

def has_permission(user, permission_name):
    
    if not user.is_authenticated:
        return False
    
    role = user.role
    if role is None:
        return False
    
    return role.permissions.filter(name = permission_name).exists()