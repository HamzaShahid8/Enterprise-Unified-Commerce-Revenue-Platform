from django.db import models
from .models import *

class ActiveProductVariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class DeleteProductVariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
class AllProductVariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeleteProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
class AllProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeleteCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
class AllCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
class ActiveBrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeleteBrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)
    
class AllBrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()