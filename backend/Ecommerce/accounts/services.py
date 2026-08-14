from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class GoogleAuthService:

    @staticmethod
    @transaction.atomic
    def authenticate(google_token):
        
        # verify token
        try:
            paylaod = id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
            
        except Exception:
            raise AuthenticationFailed('Invalid Google Token.')
        
        # verify google email
        if not paylaod.get('email_verified', False):
            raise AuthenticationFailed('Google email is not verified.')
        
        email = paylaod['email']
        first_name = paylaod.get("given_name", "")
        last_name = paylaod.get("family_name", "")
        picture = paylaod.get("picture", "")
        
        # get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults = {
                'username': get_random_string(12),
                'first_name': first_name,
                'last_name': last_name,
                'is_email_verified': True,
            },
        )
        
        # existing user
        if not created:
            
            updated = False
            
            if not user.is_email_verified:
                user.is_email_verified = True
                updated = True
                
            if not first_name and user.first_name != first_name:
                user.first_name = first_name
                updated = True
                
            if not last_name and user.last_name != last_name:
                user.last_name = last_name
                updated = True
                
            if updated:
                user.save(
                    update_fields=[
                        'is_email_verified',
                        'first_name',
                        'last_name',
                    ]
                )
                
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return {
            "user": user,
            "access": access,
            "refresh": str(refresh),
            "data": {
                "message": "Google login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "picture": picture,
                },
            },
        }