from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.carts.utils import get_user_cart
from app.orders.models import Order, OrderItem
from app.orders.utils import generate_order_number


@login_required
def checkout_page(request):
    cart = get_user_cart(request)
    items = cart.items.filter(is_deleted=False)
    total = sum(item.total_price for item in items)

    # Fetch user's saved addresses
    addresses = request.user.addresses.filter(is_deleted=False)

    if request.method == "POST":
        address_id = request.POST.get("address_id")

        if not address_id:
            messages.error(request, "Please select an address.")
            return redirect("checkout_page")

        # Get selected address
        selected_address = request.user.addresses.get(id=address_id)

        # Create order
        order = Order.objects.create(
        user=request.user,
        address=selected_address,
        order_no=generate_order_number(),
        total_amount=total,
    )

        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.total_price,
            )

        # Clear cart (soft delete items)
        cart.items.update(is_deleted=True)

        messages.success(request, "Order placed successfully!")
        return redirect("order_success_page", order_no=order.order_no)

    return render(request, "orders/checkout_page.html", {
        "cart": cart,
        "items": items,
        "total": total,
        "addresses": addresses,   # 👉 pass addresses to template
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