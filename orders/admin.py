from django.contrib import admin
from .models import Customer, Order, OrderItem


# ================================
# ORDER ITEMS
# ================================

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

    def subtotal(self, obj):

        if obj.price is None:
            return 0

        return obj.price * obj.quantity

    subtotal.short_description = "Subtotal"


# ================================
# ORDERS
# ================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_display",
        "products_display",
        "total_price",
        "payment_option",
        "payment_status",
        "status",
        "created_at",
    )

    list_editable = (
        "payment_status",
        "status",
    )

    list_filter = (
        "payment_option",
        "payment_status",
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer__name",
        "customer__phone",
        "customer__email",
        "items__product__name",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "order_number",
        "total_price",
        "created_at",
    )

    inlines = [
        OrderItemInline,
    ]

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "customer",
                    "total_price",
                )
            },
        ),
        (
            "Payment",
            {
                "fields": (
                    "payment_option",
                    "payment_status",
                )
            },
        ),
        (
            "Order Status",
            {
                "fields": (
                    "status",
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

    def customer_display(self, obj):

        return (
            obj.customer.name
            or obj.customer.phone
            or "WhatsApp Customer"
        )

    customer_display.short_description = "Customer"

    def products_display(self, obj):

        products = obj.items.select_related("product")

        return ", ".join(
            f"{item.product.name} × {item.quantity}"
            for item in products
        )

    products_display.short_description = "Products"


# ================================
# CUSTOMERS
# ================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "order_count",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    def order_count(self, obj):

        return obj.orders.count()

    order_count.short_description = "Orders"