from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from roles_permissions.models import Roles

# User_Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_email_verified', 'password', 'role']
        read_only_fields = ['id']
        
    # validation on email
    def validate_email(self, email):
        if not email.endswith('@gmail.com'):
            raise serializers.ValidationError('Email must be a Gmail address.')
        return email
    
    # create user
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        role_name = Roles.objects.get(name='customer')
        
        user = User.objects.create(
            role=role_name,
            is_email_verified=False,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
    
# login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(
            username = data['email'],
            password = data['password']
        )
        
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        
        data['user'] = user
        return data
    
# OTP serializer
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'email', 'otp', 'is_verified', 'created_at', 'expires_at']
        read_only_fields = ['id', 'is_verified', 'created_at', 'expires_at']
        
# google token
class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField()