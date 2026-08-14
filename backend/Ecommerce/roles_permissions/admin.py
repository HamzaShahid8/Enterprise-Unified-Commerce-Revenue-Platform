from django.contrib import admin
from .models import Permissions, Roles


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "name",
    )
    ordering = (
        "id",
    )


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "permissions__name",
    )
    search_fields = (
        "name",
        "permissions__name",
    )
    list_filter = (
        "permissions",
    )
    filter_horizontal = (
        "permissions",
    )
    ordering = (
        "id",
    )