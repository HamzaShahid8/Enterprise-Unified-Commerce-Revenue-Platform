from django.db import models
from accounts.models import User
from roles_permissions.models import *
from profiles.models import *
from products.models import *
from orders.models import *
from billing.models import *

# Create your models here.

class ActivityLogs(models.Model):
    
    ACTION_STATUS = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('restore', 'Restore'),
        ('payment', 'Payment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_activity_logs', null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_STATUS, null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    object_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"