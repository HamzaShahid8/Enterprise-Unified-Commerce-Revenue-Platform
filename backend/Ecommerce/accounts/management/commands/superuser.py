from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser.'
    
    def handle(self, *args, **kwargs):
        
        username = os.getenv('SUPERUSER_USERNAME')
        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')
        
        if not username or not password or not email:
            self.stdout.write(self.style.ERROR('Enter credentials'))
            
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
            
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))