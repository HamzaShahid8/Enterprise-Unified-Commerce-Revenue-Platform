from django.db import models
from .models import *

class ActiveCustomerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
        
class DeleteCustomerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
        
class AllCustomerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset()
        
class ActiveManagerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
        
class DeleteManagerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
        
class AllManagerProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset()
        
class ActiveEmployeeProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
        
class DeleteEmployeeProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
        
class AllEmployeeProfileManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset()