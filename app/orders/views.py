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
    cart = get_user_cart(request)
    items = cart.items.filter(is_deleted=False).select_related('product')

    # Check stock before showing checkout
    for item in items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Not enough stock for {item.product.name}.")
            return redirect("cart_page")

    total = sum(item.total_price for item in items)

    addresses = request.user.addresses.filter(is_deleted=False).order_by('-is_default', '-created_at')

    selected_id = None
    default_addr = addresses.filter(is_default=True).first()
    if default_addr:
        selected_id = default_addr.id
    elif addresses:
        selected_id = addresses.first().id

    if request.method == "POST":
        address_id = request.POST.get("address")
        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect("checkout_page")

        address = get_object_or_404(Address, id=address_id, user=request.user, is_deleted=False)

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            order_no=generate_order_number(),
            total_amount=total,
        )

        # Create order items + reduce stock
        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.total_price,
            )

            item.product.stock -= item.quantity

            # Optional: Make product inactive if out of stock
            if item.product.stock <= 0:
                item.product.stock = 0
                item.product.is_active = False

            item.product.save()

        # Empty cart (soft delete)
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

    # Prevent Buy Now if out of stock
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product.slug)

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

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=price,
            subtotal=price,
        )

        product.stock -= 1
        if product.stock <= 0:
            product.stock = 0
            product.is_active = False
        product.save()

        messages.success(request, "Order placed successfully!")
        return redirect("order_success_page", order_no=order.order_no)

    return render(request, "orders/buy_now_page.html", {
        "product": product,
        "addresses": addresses,
        "price": price,
    })


@login_required
def cancel_order(request, order_id):
    # Load the order
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Stop if already cancelled or delivered
    if order.order_status in ["delivered", "cancelled"]:
        messages.error(request, "This order cannot be cancelled.")
        return redirect("order_detail_page", order_id=order.id)

    # Restore stock for each item
    for item in order.items.all():
        product = item.product
        product.stock += item.quantity
        product.save()

    # Update order status
    order.order_status = "cancelled"
    order.save()

    messages.success(request, "Order cancelled successfully & stock restored.")
    return redirect("order_detail_page", order_id=order.id)