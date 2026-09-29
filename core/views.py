from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from store.models import Product, Category
from django.db.models import Q
from django.db.models import Count, Sum
from orders.models import Customer, Order


def home(request):
    categories = Category.objects.all()

    category_products = {}

    for category in categories:
        products = Product.objects.filter(
            category=category,
            is_available=True
        )[:6]

        category_products[category] = products

    context = {
        "categories": categories,
        "category_products": category_products,
    }

    return render(
        request,
        "core/home.html",
        context
    )

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    deposit_amount = product.price * Decimal("0.80")

    return render(
        request,
        "core/product_detail.html",
        {
            "product": product,
            "deposit_amount": deposit_amount,
        }
    )
def category_products(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    return render(
        request,
        "core/category_products.html",
        {
            "category": category,
            "products": products,
        }
    )

def product_list(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.filter(
        is_available=True
    )

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(
        request,
        "core/product_list.html",
        {
            "products": products,
            "query": query,
        }
    )
def about(request):
    return render(
        request,
        "core/about.html"
    )
def contact(request):
    return render(
        request,
        "core/contact.html"
    )

def dashboard(request):

    total_orders = Order.objects.count()

    total_products = Product.objects.filter(
        is_available=True
    ).count()

    total_customers = Customer.objects.count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    completed_orders = Order.objects.filter(
        status="completed"
    ).count()

    # Calculate actual recorded payments.
    paid_sales = Order.objects.filter(
        payment_status="paid"
    ).aggregate(
        total=Sum("total_price")
    )["total"] or Decimal("0.00")

    partial_orders = Order.objects.filter(
        payment_status="partial"
    )

    partial_sales = Decimal("0.00")

    for order in partial_orders:

        if order.payment_option == "deposit":
            partial_sales += order.total_price * Decimal("0.80")

        else:
            partial_sales += order.total_price

    total_sales = paid_sales + partial_sales

    recent_orders = Order.objects.select_related(
        "customer"
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-created_at"
    )[:5]

    recent_customers = Customer.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "total_orders": total_orders,
        "total_products": total_products,
        "total_customers": total_customers,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_sales": total_sales,
        "recent_orders": recent_orders,
        "recent_customers": recent_customers,
    }

    return render(
        request,
        "core/dashboard.html",
        context
    )

def payment(request):
    return render(
        request,
        "core/payment.html"
    )