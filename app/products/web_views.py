from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator
from app.wishlist.models import Wishlist



def product_list_page(request, slug=None):
    category = None
    page_title = "All Products"
    products = Product.objects.filter(is_deleted=False)

    # Filter by category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
        page_title = category.name

    # Sort logic
    sort = request.GET.get("sort")
    if sort == "low":
        products = products.order_by("discount_price", "price")
    elif sort == "high":
        products = products.order_by("-discount_price", "-price")
    elif sort == "new":
        products = products.order_by("-created_at")

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ---- WISHLIST IDs ----
    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list("product_id", flat=True)

    return render(request, "products/product_list.html", {
        "products": page_obj,
        "categories": Category.objects.filter(is_deleted=False),
        "page_title": page_title,
        "wishlist_ids": wishlist_ids,
    })

def product_detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True, is_deleted=False)

    wishlist_exists = False
    if request.user.is_authenticated:
        wishlist_exists = Wishlist.objects.filter(
            user=request.user, product=product
        ).exists()

    return render(request, "products/product_detail.html", {
        "product": product,
        "wishlist_exists": wishlist_exists,
    })

def home_page(request):
    categories = Category.objects.filter(is_deleted=False)
    category_data = []
                    
    for category in categories:
        products = Product.objects.filter(
            category=category, 
            is_active=True, 
            is_deleted=False
        )[:6]

        category_data.append({
            "category": category,
            "products": products
        })

    return render(request, "products/home.html", {"category_data": category_data})


def product_search(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query, is_deleted=False)
    return render(request, "products/product_list.html", {"products": products, "search": query})