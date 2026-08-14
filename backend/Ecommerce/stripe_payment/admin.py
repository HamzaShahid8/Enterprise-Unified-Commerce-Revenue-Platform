from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    
    # LIST VIEW
    list_display = (
        "payment_id",
        "order_link",
        "get_username",
        "provider_badge",
        "payment_intent",
        "amount_display",
        "currency",
        "status_badge",
        "created_at",
    )
    
    def get_username(self, obj):
        return obj.order.user.username
    
    get_username.short_description='Username'

    list_display_links = (
        "payment_id",
        "payment_intent",
    )

    # FILTERS
    list_filter = (
        "provider",
        "status",
        "currency",
        "created_at",
    )

    # SEARCH
    search_fields = (
        "payment_intent_id",
        "order__code",
        "order__id",
        "order__user__email",
        "order__user__first_name",
        "order__user__last_name",
    )

    # DATE HIERARCHY
    date_hierarchy = "created_at"

    # DEFAULT ORDERING
    ordering = (
        "-created_at",
    )

    
    # PAGINATION
    list_per_page = 25

    
    # READONLY FIELDS
    readonly_fields = (
        "payment_intent_id",
        "created_at",
        "updated_at",
        "payment_summary",
    )

    # FORM LAYOUT
    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "payment_summary",
                    "order",
                    "provider",
                    "status",
                )
            },
        ),

        (
            "Stripe Information",
            {
                "fields": (
                    "payment_intent_id",
                )
            },
        ),

        (
            "Amount",
            {
                "fields": (
                    "amount",
                    "currency",
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

    # OPTIMIZED QUERYSET
    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.select_related(
            "order",
            "order__user",
        )

    # PAYMENT ID

    @admin.display(
        description="Payment ID",
        ordering="id",
    )
    def payment_id(self, obj):

        return str(obj.id)[:12]

  

    @admin.display(
        description="Order",
    )
    def order_link(self, obj):

        if not obj.order:
            return "-"

        return obj.order.code

    

    @admin.display(
        description="Customer",
    )
    def customer_name(self, obj):

        if not obj.order or not obj.order.user:
            return "-"

        user = obj.order.user

        full_name = (
            f"{user.first_name} "
            f"{user.last_name}"
        ).strip()

        return full_name or user.email

  

    @admin.display(
        description="Payment Intent",
    )
    def payment_intent(self, obj):

        if not obj.payment_intent_id:
            return "-"

        return obj.payment_intent_id

   

    @admin.display(
        description="Provider",
    )
    def provider_badge(self, obj):

        return format_html(
            '<span style="'
            'background:#635bff;'
            'color:white;'
            'padding:4px 8px;'
            'border-radius:12px;'
            'font-weight:600;'
            '">'
            '{}'
            '</span>',
            obj.get_provider_display(),
        )

    

    @admin.display(
        description="Status",
        ordering="status",
    )
    def status_badge(self, obj):

        status_styles = {
            "pending": (
                "#f59e0b",
                "#fff7ed",
            ),
            "processing": (
                "#2563eb",
                "#eff6ff",
            ),
            "succeeded": (
                "#16a34a",
                "#f0fdf4",
            ),
            "failed": (
                "#dc2626",
                "#fef2f2",
            ),
            "cancelled": (
                "#6b7280",
                "#f3f4f6",
            ),
        }

        color, background = status_styles.get(
            obj.status,
            (
                "#374151",
                "#f9fafb",
            ),
        )

        return format_html(
            '<span style="'
            'color:{};'
            'background:{};'
            'padding:4px 10px;'
            'border-radius:12px;'
            'font-weight:600;'
            'font-size:12px;'
            '">'
            '{}'
            '</span>',
            color,
            background,
            obj.get_status_display(),
        )

   

    @admin.display(
        description="Amount",
        ordering="amount",
    )
    def amount_display(self, obj):

        if obj.amount is None:
            return "-"

        return f"{obj.amount:,.2f}"

   

    @admin.display(
        description="Payment Summary",
    )
    def payment_summary(self, obj):

        return format_html(
            """
            <div style="
                padding:15px;
                background:#f8fafc;
                border:1px solid #e5e7eb;
                border-radius:8px;
            ">
                <strong>Payment Intent:</strong> {}<br>
                <strong>Provider:</strong> {}<br>
                <strong>Amount:</strong> {} {}<br>
                <strong>Status:</strong> {}
            </div>
            """,
            obj.payment_intent_id or "-",
            obj.get_provider_display(),
            obj.amount or "0.00",
            obj.currency.upper() if obj.currency else "",
            obj.get_status_display(),
        )