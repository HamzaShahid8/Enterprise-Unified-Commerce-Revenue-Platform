from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from datetime import timedelta
from django.utils import timezone

# Create your models here.

# BaseModel
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
# User
class User(AbstractUser, BaseModel):
    role = models.ForeignKey('roles_permissions.Roles', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} - {self.email}"
    
    
# OTP
class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))
        
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        
        super().save(*args, **kwargs)