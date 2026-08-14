from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from accounts.models import *

@receiver(post_save, sender = User)
def profile(sender, instance, created, **kwargs):
    if created:
        if instance.role and instance.role.name == 'manager':
            ManagerProfile.objects.get_or_create(user=instance)
            
        elif instance.role and instance.role.name == 'employe':
            EmployeeProfile.objects.get_or_create(user=instance)
            
        elif instance.role and instance.role.name == 'customer':
            CustomerProfile.objects.get_or_create(user=instance)
            
        else:
            print('Unknown role')