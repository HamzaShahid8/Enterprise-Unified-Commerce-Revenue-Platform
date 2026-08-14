from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Roles

@receiver(post_migrate)
def sync_groups(sender, **kwargs):
    for role in Roles.objects.filter(name__in = ['manager', 'employe']):
        Group.objects.get_or_create(name=role.name)