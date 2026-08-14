from django.db import models
import uuid
from profiles.models import UUID
from accounts.models import BaseModel
from .managers import *

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveCategoryManager()
    deleted_objects = DeleteCategoryManager()
    all_objects = AllCategoryManager()
    
    def __str__(self):
        return f"{self.name} - {self.is_deleted}"
    
class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveBrandManager()
    deleted_objects = DeleteBrandManager()
    all_objects = AllBrandManager()
    
    def __str__(self):
        return f"{self.name} - {self.is_deleted}"
    
class Product(UUID, BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_brand')
    stock = models.PositiveIntegerField(blank=True, null=True, default=20)
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveProductManager()
    deleted_objects = DeleteProductManager()
    all_objects = AllProductManager()
    
    def __str__(self):
        return f"{self.code} - {self.name} - {self.category} - {self.brand} - {self.stock} - {self.is_deleted}"
    
class ProductVariant(BaseModel, UUID):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = ActiveProductVariantManager()
    deleted_objects = DeleteProductVariantManager()
    all_objects = AllProductVariantManager()
    
    def __str__(self):
        return f"{self.code} - {self.product.name} - {self.is_deleted}"