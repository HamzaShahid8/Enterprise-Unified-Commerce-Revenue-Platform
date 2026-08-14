from django.urls import path, include
from .views import OrderViewSet, OrderItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('order', OrderViewSet, basename='create-order')
router.register('order-item', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
]