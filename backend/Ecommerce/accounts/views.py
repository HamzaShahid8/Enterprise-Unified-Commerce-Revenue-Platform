from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .throttles import *
from .tasks import *
from celery.result import AsyncResult
from .services import *
from .permissions import IsEmailVerified
from monitoring.models import ActivityLogs
from monitoring.utils import create_log
from django.db import connection
from django.core.cache import cache
from celery import current_app

# Create your views here.

# Register View
class RegisterView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]
    
    def perform_create(self, serializer):
        serializer.save()
    
# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(username=email, password=password)
        
        if user is None:

            return Response({
                'error': 'Invalid email or password.'
            }, status=status.HTTP_404_NOT_FOUND)
            
        if not user.is_email_verified:
            otp_obj = OTP.objects.create(email=user.email)
            send_otp.delay(otp_obj.id)
        
            return Response({
                'message': 'OTP sent successfully.',
                'email': user.email
            })
        
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        create_log(
            user=user,
            action='login',
            model_name='User',
            object_id=user.id,
            description=f"User {user.username} logged in successfully."
        )
        
        response = Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )
        
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        return response
    
# Refresh token
class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        refresh_token = request.COOKIES.get('refresh_token')
        
        try:
            if refresh_token is None:
                return Response({
                    'error': 'Refresh token not found.'
                }, status=status.HTTP_404_NOT_FOUND)
                
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            response = Response({
                'message': 'Access token refreshed successfully.'
            }, status=status.HTTP_201_CREATED)
            
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )
            
            return response
        
        except (TokenError):
            return Response({
                'message': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)
            
# password change
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        if not user.check_password(request.data['old_password']):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(request.data['new_password'])
        user.save()
        return Response({
            'message': 'Password has changed successfully.'
        }, status=status.HTTP_201_CREATED)
        
# Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        user = self.request.user
        
        create_log(
            user=user,
            action='logout',
            model_name='User',
            object_id=user.id,
            description=f"User {user.username} logout."
        )
        
        response = Response({
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    
# Dashboard
class DashboardView(APIView):
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get(self, request):
        user = request.user
        
        return Response({
            'message': f"Welcome {user.username} to out platform.",
            'email': f"Your email is {user.email}"
        })
        
# OTP generate
class GenerateOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        email = request.data.get('email')
        
        otp_obj = OTP.objects.create(email=email)
        
        task = send_otp.delay(otp_obj.id)
        
        return Response({
            'message': 'OTP generated and sent.',
            'message': f"OTP sent to {otp_obj.id}"
        })
        
# Verify OTP
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        try:
            otp_obj = OTP.objects.filter(email=email, otp=otp).latest('created_at')
            otp_obj.is_verified = True
            otp_obj.save()
            
            user = User.objects.get(email=email)
            
            user.is_email_verified = True
            user.save(update_fields=['is_email_verified'])
            
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            
            response = Response({
                "message": "OTP verified successfully.",
                "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                },
            })
            
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh_token),
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
            )

            return response
            
        except OTP.DoesNotExist:
            return Response({
                'Invalid email or otp'
            }, status=status.HTTP_400_BAD_REQUEST)
            

# google oauth
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = GoogleAuthService.authenticate(
            serializer.validated_data["token"]
        )

        response = Response(result["data"])

        response.set_cookie(
            key="access_token",
            value=result["access"],
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        response.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        return response
    
class HealthyCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        
        health = {
            'status': 'healthy',
            'database': 'connected',
            'redis': 'connected',
            'celery': 'running',
        }
        
        status_code = status.HTTP_200_OK
        
        # database
        try:
            connection.ensure_connection()
            
        except Exception as e:
            health['status'] = 'unhealthy'
            health['database'] = str(e)
            
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        # redis
        try:
            cache.set('health_check', 'ok', timeout=10)
            cache.get('health_check')
            
        except Exception as e:
            health['status'] = 'unhealthy'
            health['redis'] = str(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        # celery
        try:
            current_app.control.ping(timeout=10)
        except Exception as e:
            health['status'] = 'unhealthy'
            health['celery'] = str(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        return Response(health, status=status_code)