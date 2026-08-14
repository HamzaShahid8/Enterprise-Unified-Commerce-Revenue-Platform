from django.contrib import admin
from .models import (
    CustomerProfile,
    ManagerProfile,
    EmployeeProfile,
)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "user",
        "phone",
        "cnic",
        "city",
        "country",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "is_deleted",
        "city",
        "country",
        "created_at",
    )

    search_fields = (
        "code",
        "user__username",
        "user__email",
        "phone",
        "cnic",
        "city",
        "country",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("User Information", {
            "fields": (
                "user",
                "code",
            )
        }),
        ("Customer Details", {
            "fields": (
                "phone",
                "cnic",
                "address",
                "city",
                "country",
            )
        }),
        ("Status", {
            "fields": (
                "is_deleted",
            )
        }),
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "user",
        "department",
        "designation",
        "phone",
        "joining_date",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "department",
        "designation",
        "is_deleted",
        "joining_date",
    )

    search_fields = (
        "code",
        "user__username",
        "user__email",
        "department",
        "designation",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("User Information", {
            "fields": (
                "user",
                "code",
            )
        }),
        ("Employment Details", {
            "fields": (
                "department",
                "designation",
                "phone",
                "joining_date",
            )
        }),
        ("Status", {
            "fields": (
                "is_deleted",
            )
        }),
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "user",
        "department",
        "designation",
        "contact",
        "phone",
        "joining_date",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "department",
        "designation",
        "is_deleted",
        "joining_date",
    )

    search_fields = (
        "code",
        "user__username",
        "user__email",
        "department",
        "designation",
        "contact",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "code",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("User Information", {
            "fields": (
                "user",
                "code",
            )
        }),
        ("Employment Details", {
            "fields": (
                "contact",
                "department",
                "designation",
                "phone",
                "joining_date",
            )
        }),
        ("Status", {
            "fields": (
                "is_deleted",
            )
        }),
        ("Audit", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )