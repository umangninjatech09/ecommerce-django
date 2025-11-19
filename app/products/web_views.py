from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator



def product_list_page(request, slug=None):
    category = None
    page_title = "All Products"

    products = Product.objects.filter(is_deleted=False)

    # Filter by category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
        page_title = category.name

    # Sorting
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

    return render(request, "products/product_list.html", {
        "products": page_obj,
        "categories": Category.objects.filter(is_deleted=False),
        "page_title": page_title,
    })

def product_detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True, is_deleted=False)
    return render(request, "products/product_detail.html", {"product": product})


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