from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.products.models import Product
from app.carts.models import CartItem
from app.carts.utils import get_user_cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    cart = get_user_cart(request)

    # Check active cart item only
    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product,
        is_deleted=False
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            price=product.discount_price or product.price
        )

    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.META.get("HTTP_REFERER", "home_page"))


def cart_page(request):
    cart = get_user_cart(request)
    items = cart.items.filter(is_deleted=False)
    total = sum(item.total_price for item in items)

    return render(request, "cart/cart_page.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, is_deleted=False)
    quantity = int(request.POST.get("quantity"))

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    return redirect("cart_page")


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, is_deleted=False)
    item.delete()
    return redirect("cart_page")
