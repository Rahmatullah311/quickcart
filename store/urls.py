from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("order/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("api/quick-order/", views.quick_order_api, name="quick_order_api"),
]
