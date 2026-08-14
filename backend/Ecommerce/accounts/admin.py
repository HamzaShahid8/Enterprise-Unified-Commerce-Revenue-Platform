from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        'role',
        "is_email_verified",
        "is_active",
        "is_staff",
        "last_login",
        "created_at",
    )

    list_filter = (
        'role',
        "is_email_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "last_login",
        "date_joined",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Account Information", {
            "fields": (
                "email",
                "username",
                "password",
                'role',
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
            )
        }),

        ("Verification", {
            "fields": (
                "is_email_verified",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "otp",
        "is_verified",
        "expires_at",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "created_at",
    )

    search_fields = (
        "email",
        "otp",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "otp",
        "created_at",
        "expires_at",
    )