from django.contrib import admin
from .models import Category, Brand, Product, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "image",
        "price",
        "color",
        "size",
        "is_deleted",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "code",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        return Category.all_objects.all()

    actions = ["soft_delete", "restore"]

    @admin.action(description="Soft Delete Selected Categories")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore Selected Categories")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        return Brand.all_objects.all()

    actions = ["soft_delete", "restore"]

    @admin.action(description="Soft Delete Selected Brands")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore Selected Brands")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "category",
        "brand",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "is_deleted",
    )

    search_fields = (
        "code",
        "name",
        "category__name",
        "brand__name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "code",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "category",
        "brand",
    )

    inlines = [ProductVariantInline]

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "brand",
                    "description",
                    "is_deleted",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "id",
                    "code",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_queryset(self, request):
        return Product.all_objects.select_related(
            "category",
            "brand"
        )

    actions = ["soft_delete", "restore"]

    @admin.action(description="Soft Delete Selected Products")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore Selected Products")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "product",
        "price",
        "color",
        "size",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "is_deleted",
        "color",
        "size",
    )

    search_fields = (
        "code",
        "product__name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "code",
        "created_at",
        "updated_at",
    )

    list_select_related = ("product",)

    def get_queryset(self, request):
        return ProductVariant.all_objects.select_related("product")

    actions = ["soft_delete", "restore"]

    @admin.action(description="Soft Delete Selected Variants")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore Selected Variants")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)