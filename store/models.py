from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField  # Import this


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("نام محصول"))
    description = RichTextField(verbose_name=_("توضیحات"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("قیمت (افغانی)")
    )
    image = models.ImageField(
        upload_to="products/", null=True, blank=True, verbose_name=_("تصویر")
    )
    stock = models.IntegerField(default=0, verbose_name=_("موجودی"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", _("در انتظار")),
        ("confirmed", _("تایید شده")),
        ("shipped", _("ارسال شده")),
        ("delivered", _("تحویل داده شده")),
        ("cancelled", _("لغو شده")),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("محصول")
    )
    quantity = models.IntegerField(verbose_name=_("تعداد"))
    customer_name = models.CharField(max_length=200, verbose_name=_("نام مشتری"))
    # Remove customer_email field - just comment or delete it
    # customer_email = models.EmailField(verbose_name=_('ایمیل مشتری'))
    customer_phone = models.CharField(max_length=20, verbose_name=_("شماره تماس"))
    address = models.TextField(verbose_name=_("آدرس"))
    special_instructions = models.TextField(blank=True, verbose_name=_("توضیحات ویژه"))
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("قیمت کل")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("وضعیت"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت"))

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارشات")

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"سفارش {self.id} - {self.customer_name}"
