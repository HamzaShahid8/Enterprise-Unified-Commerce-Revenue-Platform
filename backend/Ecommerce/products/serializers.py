from rest_framework import serializers
from .models import Brand, Category, Product, ProductVariant

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted']
        
class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]
        
class BrandReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'is_deleted']
        
class BrandWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']
        
class ProductVariantReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['code', 'image', 'price', 'color', 'size', 'is_deleted', 'created_at', 'updated_at']
        
class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    product_variants = ProductVariantReadSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'brand', 'stock', 'is_deleted', 'product_variants', 'description']
        
class ProductVariantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['image', 'price', 'color', 'size']
        
class ProductWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset = Category.objects.filter(is_deleted=False), slug_field='name')
    brand = serializers.SlugRelatedField(queryset = Brand.objects.filter(is_deleted=False), slug_field='name')
    items = ProductVariantWriteSerializer(many=True, write_only=True, source='product_variants', required=False)
    
    class Meta:
        model = Product
        fields = ['name', 'category','brand', 'items', 'description']