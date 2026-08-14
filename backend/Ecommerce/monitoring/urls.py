from django.urls import path, include
from .views import ActivityLogsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('activity_logs', ActivityLogsViewSet, basename='activity_logs')

urlpatterns = router.urls