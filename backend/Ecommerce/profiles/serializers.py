from rest_framework import serializers
from .models import CustomerProfile, ManagerProfile, EmployeeProfile

class CustomerProfileReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'phone', 'address', 'cnic', 'city', 'country', 'is_deleted', 'created_at', 'updated_at']

class CustomerProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'cnic', 'city', 'country']

class ManagerProfileReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = ManagerProfile
        fields = ['id', 'user', 'department', 'phone', 'joining_date', 'designation', 'is_deleted', 'created_at', 'updated_at']
        
class ManagerProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ['department', 'phone', 'joining_date', 'designation']
        
class EmployeeProfileReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'contact', 'department', 'designation', 'phone', 'joining_date', 'is_deleted', 'created_at', 'updated_at']
        
class EmployeeProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['contact', 'department', 'designation', 'phone', 'joining_date']