from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.carts.utils import get_user_cart
from app.orders.models import Order, OrderItem
from app.orders.utils import generate_order_number
from app.products.models import Product
from app.users.models import Address




@login_required
def checkout_page(request):
    # get cart and visible items
    cart = get_user_cart(request)
    items = cart.items.filter(is_deleted=False).select_related('product')
    total = sum(item.total_price for item in items)

    # get user's saved addresses (not deleted)
    addresses = request.user.addresses.filter(is_deleted=False).order_by('-is_default', '-created_at')

    # default selected address id (first default or first address)
    selected_id = None
    default_addr = addresses.filter(is_default=True).first()
    if default_addr:
        selected_id = default_addr.id
    elif addresses:
        selected_id = addresses.first().id

    # POST: place order
    if request.method == "POST":
        address_id = request.POST.get("address")
        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect("checkout_page")

        address = get_object_or_404(Address, id=address_id, user=request.user, is_deleted=False)

        # create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            order_no=generate_order_number(),
            total_amount=total,
        )

        # create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.total_price,
            )

        # soft-delete the cart items
        cart.items.filter(is_deleted=False).update(is_deleted=True)

        messages.success(request, "Order placed successfully!")
        return redirect("order_success_page", order_no=order.order_no)

    return render(request, "orders/checkout_page.html", {
        "addresses": addresses,
        "items": items,
        "total": total,
        "selected_id": selected_id,
    })



@login_required
def order_list_page(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list_page.html", {"orders": orders})


@login_required
def order_detail_page(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "orders/order_detail_page.html", {"order": order})


@login_required
def order_success_page(request, order_no):
    order = Order.objects.get(order_no=order_no)
    return render(request, "orders/order_success.html", {"order": order})



@login_required
def buy_now_page(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    price = product.discount_price or product.price

    addresses = request.user.addresses.filter(is_deleted=False)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        address = get_object_or_404(Address, id=address_id, user=request.user)

        order = Order.objects.create(
            user=request.user,
            address=address,
            order_no=generate_order_number(),
            total_amount=price,
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=price,
            subtotal=price,
        )

        messages.success(request, "Order placed successfully!")
        return redirect("order_success_page", order_no=order.order_no)

    return render(request, "orders/buy_now_page.html", {
        "product": product,
        "addresses": addresses,
        "price": price,
    })
