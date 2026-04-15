from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from .models import Product, Order


def product_list(request):
    """Display all available products"""
    products = Product.objects.filter(is_active=True, stock__gt=0)
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, product_id):
    """Show product details and order form"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == "POST":
        # Process order
        quantity = int(request.POST.get("quantity", 1))

        if quantity > product.stock:
            messages.error(
                request,
                _("متاسفانه فقط {stock} عدد موجود است.").format(stock=product.stock),
            )
            return redirect("product_detail", product_id=product_id)

        # Create order without email
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            customer_name=request.POST.get("customer_name"),
            customer_phone=request.POST.get("customer_phone"),
            address=request.POST.get("address"),
            special_instructions=request.POST.get("special_instructions", ""),
        )

        # Reduce stock
        product.stock -= quantity
        product.save()

        messages.success(
            request,
            _("سفارش شما با موفقیت ثبت شد! شماره سفارش: {order_id}").format(
                order_id=order.id
            ),
        )
        return redirect("order_confirmation", order_id=order.id)

    return render(request, "store/product_detail.html", {"product": product})


def order_confirmation(request, order_id):
    """Show order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "store/order_confirmation.html", {"order": order})


def quick_order_api(request):
    """Simple API endpoint for mobile/JS ordering"""
    if request.method == "POST":
        import json

        data = json.loads(request.body)

        product = get_object_or_404(Product, id=data.get("product_id"))
        quantity = int(data.get("quantity", 1))

        if quantity <= product.stock:
            order = Order.objects.create(
                product=product,
                quantity=quantity,
                customer_name=data.get("customer_name"),
                customer_phone=data.get("customer_phone"),
                address=data.get("address"),
                special_instructions=data.get("special_instructions", ""),
            )
            product.stock -= quantity
            product.save()

            return JsonResponse(
                {
                    "success": True,
                    "order_id": order.id,
                    "message": _("سفارش با موفقیت ثبت شد!"),
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("موجودی کافی نیست")}, status=400
            )

    return JsonResponse({"error": _("روش مجاز نیست")}, status=405)


# ADD THIS CUSTOM 404 VIEW FUNCTION
def custom_404_view(request, exception):
    """Custom 404 error page"""
    # Get some products to show as suggestions
    suggested_products = Product.objects.filter(is_active=True, stock__gt=0)[:4]

    return render(request, "404.html", {"products": suggested_products}, status=404)
