from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from store.models import Product
from .models import Customer, Order, OrderItem
from uuid import uuid4


def create_order(request, product_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method."},
            status=405
        )

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    quantity = int(request.POST.get("quantity", 1))
    payment_option = request.POST.get("payment_option", "deposit")

    if quantity < 1:
        return JsonResponse(
            {"error": "Invalid quantity."},
            status=400
        )

    if payment_option not in ["deposit", "full"]:
        return JsonResponse(
            {"error": "Invalid payment option."},
            status=400
        )

    total_price = product.price * quantity

    customer = Customer.objects.create()

    order = Order.objects.create(
        customer=customer,
        order_number=f"BOSKI-{uuid4().hex[:8].upper()}",
        total_price=total_price,
        payment_option=payment_option,
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price,
    )

    return JsonResponse({
        "success": True,
        "order_number": order.order_number,
    })