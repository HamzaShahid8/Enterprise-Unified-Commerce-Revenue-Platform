from django.db import models
from accounts.models import *
import uuid
from .managers import *

# Create your models here.

class UUID(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"ID-{uuid.uuid4().hex[:8].upper()}"
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.code


# customer profile
class CustomerProfile(UUID, BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    cnic = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    
    objects = ActiveCustomerProfileManager()
    deleted_objects = DeleteCustomerProfileManager()
    all_objects = AllCustomerProfileManager()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.code} - {self.user.username} - {self.cnic}"
    

# manager profile
class ManagerProfile(BaseModel, UUID):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="manager_profile",
    )
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    joining_date = models.DateField()
    designation = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    
    objects = ActiveManagerProfileManager()
    deleted_objects = DeleteManagerProfileManager()
    all_objects = AllManagerProfileManager()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.code} - {self.user.username} - {self.designation}"
    

# employee profile
class EmployeeProfile(BaseModel, UUID):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    contact = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    
    objects = ActiveEmployeeProfileManager()
    deleted_objects = DeleteEmployeeProfileManager()
    all_objects = AllEmployeeProfileManager()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.code} - {self.user.username} - {self.department}"