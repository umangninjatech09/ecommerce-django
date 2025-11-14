from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list_page(request):
    products = Product.objects.filter(is_active=True, is_deleted=False)
    return render(request, "products/product_list.html", {"products": products})


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


