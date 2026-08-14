from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('change-password/', ChangePasswordView.as_view(), name = 'change-password'),
    path('refresh/', RefreshTokenView.as_view(), name = 'refresh'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
    path('generate-otp/', GenerateOTPView.as_view(), name = 'generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name = 'verify-otp'),
    path("google-login/", GoogleLoginView.as_view(), name="google_login"),
    path('healthy_check/', HealthyCheckView.as_view(), name = 'healthy_check'),
]