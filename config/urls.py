from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    home,
    product_detail,
    category_products,
    product_list,
    about,
    contact,
    dashboard,
    payment,
)
from orders.views import create_order


from core.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),

    path(
        "product/<int:product_id>/",
        product_detail,
        name="product_detail"
    ),
path(
    "category/<slug:slug>/",
    category_products,
    name="category_products"
),
path(
    "products/",
    product_list,
    name="product_list"
),
path(
    "about/",
    about,
    name="about"
),
path(
    "contact/",
    contact,
    name="contact"
),
path(
    "order/create/<int:product_id>/",
    create_order,
    name="create_order"
),
path(
    "dashboard/",
    dashboard,
    name="dashboard"
),
path(
    "payment/",
    payment,
    name="payment"
),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )