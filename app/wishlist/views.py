from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.products.models import Product
from .models import Wishlist


@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist/wishlist_page.html", {"items": items})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_deleted=False)

    item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if created:
        messages.success(request, " ✔ Added to your Wishlist")
    else:
        item.delete()
        messages.info(request, "Removed from your Wishlist")

    return redirect(request.META.get("HTTP_REFERER", "home_page"))
