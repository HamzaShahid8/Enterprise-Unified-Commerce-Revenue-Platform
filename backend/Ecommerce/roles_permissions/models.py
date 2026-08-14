from django.db import models

# Create your models here.

# permissions
class Permissions(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name
    
# roles
class Roles(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    permissions = models.ManyToManyField(Permissions)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name