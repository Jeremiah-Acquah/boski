from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "product_count",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_available",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
        "category__name",
    )

    list_editable = (
        "price",
        "is_available",
        "is_featured",
    )

    autocomplete_fields = (
        "category",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Pricing & Availability",
            {
                "fields": (
                    "price",
                    "is_available",
                    "is_featured",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )