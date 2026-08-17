from django.shortcuts import render
from .services import *
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from roles_permissions.permissions import *
from roles_permissions.services import *
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from monitoring.models import ActivityLogs
from monitoring.utils import create_log
from django.core.cache import cache

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    filterset_fields = ['id', 'name']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CategoryReadSerializer
        return CategoryWriteSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name in ['manager', 'employe']:
            category = serializer.save()
        else:
            category = serializer.save()
            
        create_log(
            user=user,
            action='create',
            model_name='Category',
            object_id=category.id,
            description=f"Category {category.name} created"
        )
        
        def perform_update(self, serializer):
        
            category = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='Category',
                object_id=category.id,
                description=f"Category {category.name} updated"
            )
            
        def perform_destroy(self, instance):
        
            category_id = instance.id
            category_name = instance.name
        
            create_log(
                user=self.request.user,
                action='delete',
                model_name='Category',
                object_id=category_id,
                description=f"Category {category_name} deleted"
            )
        
            instance.delete()
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_category'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_category'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_category'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_category'
            
        return [IsAuthenticated(), permission]
            

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    filterset_fields = ['id', 'name']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['-id']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BrandReadSerializer
        return BrandWriteSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name in ['manager', 'employe']:
            brand = serializer.save()
        else:
            brand = serializer.save()
            
        create_log(
            user=user,
            action='create',
            model_name='Brand',
            object_id=brand.id,
            description=f"Brand {brand.name} created"
        )
        
        def perform_update(self, serializer):
        
            brand = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='Brand',
                object_id=brand.id,
                description=f"Brand {brand.name} updated"
            )
            
        def perform_destroy(self, instance):
        
            brand_id = instance.id
            brand_name = instance.name
        
            create_log(
                user=self.request.user,
                action='delete',
                model_name='Brand',
                object_id=brand_id,
                description=f"Brand {brand_name} deleted"
            )
        
            instance.delete()
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_brand'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_brand'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_brand'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_brand'
            
        return [IsAuthenticated(), permission]
            
            
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    lookup_field= 'code'
    
    filterset_fields = ['code', 'name', 'category', 'brand', 'stock', 'description']
    search_fields = ['code', 'name', 'category', 'brand', 'stock', 'created_at', 'updated_at']
    ordering_fields = ['code', 'name', 'stock']
    ordering = ['-code']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductReadSerializer
        return ProductWriteSerializer
    
    def list(self, request, *args, **kwargs):
        
        query_params = request.query_params.urlencode()
        
        cache_key = f"products:{query_params}"
        
        cached_data = cache.get(cache_key)
        
        # database ko hit ni krengy agr redis may h data available
        if cached_data is not None:
            return Response(cached_data)
        
        # else database ko hit
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            
            cache.set(
                cache_key,
                response.data,
                timeout=60
            )
            
            return Response
        
        serializer = self.get_serializer(queryset, many=True)
        
        cache.set(
            cache_key,
            serializer.data,
            timeout=60
        )
        
        return Response(
            serializer.data
        )
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = ProductService.create(serializer.validated_data)
        
        create_log(
            user=request.user,
            action='create',
            model_name='Product',
            object_id=product.id,
            description=(
                f"Product '{product.name}' "
                f"({product.code}) created."
            )
        )
        
        return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        product = ProductService.update(
            serializer.instance,
            serializer.validated_data
        )
        create_log(
            user=self.request.user,
            action='update',
            model_name='Product',
            object_id=product.id,
            description=(
                f"Product '{product.name}' "
                f"({product.code}) updated."
            )
        )
        
    def perform_destroy(self, instance):
        product_id = instance.id
        product_name = instance.name
        product_code = instance.code

        create_log(
            user=self.request.user,
            action='delete',
            model_name='Product',
            object_id=product_id,
            description=(
                f"Product '{product_name}' "
                f"({product_code}) deleted."
            )
        )
        ProductService.delete(instance)
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_product'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_product'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_product'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_product'
            
        return [IsAuthenticated(), permission]
            
            
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    lookup_field = 'code'
    
    filter_backends = DjangoFilterBackend, SearchFilter, OrderingFilter
    
    filterset_fields = ['code', 'product', 'price', 'color', 'size', 'created_at', 'updated_at']
    search_fields = ['code', 'price', 'color', 'size', 'created_at']
    ordering_fields = ['code', 'size', 'price']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductVariantReadSerializer
        return ProductVariantWriteSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name == 'manager':
            variant = serializer.save()
        else:
            variant = serializer.save()
            
        create_log(
            user=user,
            action='create',
            model_name='ProductVariant',
            object_id=variant.id,
            description='Product variant created'
        )
        
        def perform_update(self, serializer):
        
            variant = serializer.save()
        
            create_log(
                user=self.request.user,
                action='update',
                model_name='ProductVariant',
                object_id=variant.id,
                description='Product variant updated'
            )
            
        def perform_destroy(self, instance):
        
            variant_id = instance.id
        
            create_log(
                user=self.request.user,
                action='delete',
                model_name='ProductVariant',
                object_id=variant_id,
                description='Product Variant deleted'
            )
        
            instance.delete()
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_product_variant'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_product_variant'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_product_variant'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_product_variant'
            
        return [IsAuthenticated(), permission]