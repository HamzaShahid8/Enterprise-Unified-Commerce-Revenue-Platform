from django.contrib import admin
from django.db.models import Sum
from .models import Order, OrderItem, IdempotancyKey


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = (
        "product",
        "quantity",
        "price",
        "subtotal",
    )

    readonly_fields = (
        "price",
        "subtotal",
    )

    show_change_link = True

    def has_add_permission(self, request, obj=None):
        # Order items should normally be created through Order/API service
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent accidental stock/order manipulation from admin
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "user",
        "status",
        "payment_status",
        "subtotal",
        "shipping_cost",
        "tax",
        "discount",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "code",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "code",
        "user",
        "subtotal",
        "total_amount",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "code",
                    "user",
                    "status",
                    "payment_status",
                )
            },
        ),
        (
            "Shipping",
            {
                "fields": (
                    "shipping_address",
                    "shipping_cost",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "subtotal",
                    "tax",
                    "discount",
                    "total_amount",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        OrderItemInline,
    ]

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    def has_add_permission(self, request):
        # Orders should be created through API/business logic
        return False
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "order",
        "product",
        "quantity",
        "price",
        "subtotal",
        "created_at",
    )

    search_fields = (
        "code",
        "order__code",
        "product__code",
        "product__product__name",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "code",
        "order",
        "product",
        "quantity",
        "price",
        "subtotal",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(IdempotancyKey)
class IdempotancyKeyAdmin(admin.ModelAdmin):

    list_display = (
        "key",
        "user",
        "status_code",
        "created_at",
    )

    search_fields = (
        "key",
        "user__username",
    )

    list_filter = (
        "status_code",
        "created_at",
    )

    readonly_fields = (
        "key",
        "user",
        "response_data",
        "status_code",
        "created_at",
    )