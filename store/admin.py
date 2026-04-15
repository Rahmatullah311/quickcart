from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    list_editable = ("price", "stock", "is_active")
    fieldsets = (
        (_("اطلاعات محصول"), {"fields": ("name", "description", "price", "image")}),
        (_("موجودی و وضعیت"), {"fields": ("stock", "is_active")}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "product",
        "quantity",
        "total_price",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "customer_name",
        "customer_phone",
    )  # Remove customer_email from search
    list_editable = ("status",)
    readonly_fields = ("total_price",)
    fieldsets = (
        (
            _("اطلاعات مشتری"),
            {
                "fields": (
                    "customer_name",
                    "customer_phone",
                    "address",
                )  # Remove customer_email
            },
        ),
        (
            _("اطلاعات سفارش"),
            {"fields": ("product", "quantity", "total_price", "special_instructions")},
        ),
        (_("وضعیت"), {"fields": ("status",)}),
    )
