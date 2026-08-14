from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()

router.register('roles', RolesViewSet, basename='roles')
router.register('permissions', RolesViewSet, basename='permissions')
router.register('role-permission', RolesViewSet, basename='role-permission')

urlpatterns = [
    path('', include(router.urls)),
]