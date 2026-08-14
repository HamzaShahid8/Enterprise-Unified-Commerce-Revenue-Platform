from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductVariantViewSet,
)

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="categorys")
router.register("brands", BrandViewSet, basename="brands")
router.register("products", ProductViewSet, basename="products")
router.register("product-variants", ProductVariantViewSet, basename="product-variants")

urlpatterns = [
    path("", include(router.urls)),
]