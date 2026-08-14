from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('customer-profile', CustomerProfileViewset, basename='customer-profile')
router.register('manager-profile', ManagerProfileViewset, basename='manager-profile')
router.register('employee-profile', EmployeeProfileViewset, basename='employee-profile')

urlpatterns = [
    path('', include(router.urls)),
]