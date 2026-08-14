from django.core.management import BaseCommand
from roles_permissions.models import Roles

class Command(BaseCommand):
    help = 'Create roles.'
    
    def handle(self, *args, **kwargs):
        ROLES = [
            'manager',
            'employe',
            'customer',
        ]
        
        for role_names in ROLES:
            role, created = Roles.objects.get_or_create(name=role_names)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Roles created successfully: {role_names}"))
                
            else:
                self.stdout.write(self.style.WARNING(f'Roles already exist: {role_names}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Roles successfullt seeding: {role_names}'))