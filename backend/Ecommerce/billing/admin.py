from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    # List page
    list_display = (
        "code",
        "order",
        "get_customer",
        "subtotal",
        "tax",
        "shipping_cost",
        "discount",
        "total_amount",
        "status",
        "created_at",
    )

    # Filters
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    # Search
    search_fields = (
        "code",
        "order__code",
        "order__user__username",
        "order__user__email",
    )

    # Default ordering
    ordering = (
        "-created_at",
    )

    # Pagination
    list_per_page = 25

    # Date navigation
    date_hierarchy = "created_at"

    # Read-only fields
    readonly_fields = (
        "code",
        "order",
        "subtotal",
        "tax",
        "shipping_cost",
        "discount",
        "total_amount",
        "created_at",
        "updated_at",
    )

    # Better detail layout
    fieldsets = (
        (
            "Invoice Information",
            {
                "fields": (
                    "code",
                    "order",
                    "status",
                )
            },
        ),
        (
            "Billing Summary",
            {
                "fields": (
                    "subtotal",
                    "tax",
                    "shipping_cost",
                    "discount",
                    "total_amount",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    @admin.display(
        description="Customer",
        ordering="order__user__username"
    )
    def get_customer(self, obj):
        return obj.order.user.username