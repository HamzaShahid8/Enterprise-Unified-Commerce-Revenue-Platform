from rest_framework import serializers
from .models import *

class PermissionsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'name']
        
class PermissionsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['name']
        
class RolesReadSerializer(serializers.ModelSerializer):
    permissions = PermissionsReadSerializer(many=True, read_only=True)
    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions']
        
class RolesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['name', 'permissions']