from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm


def admin_required(view_func):
    """Allow only users with is_admin=True"""
    return login_required(user_passes_test(lambda u: getattr(u, "is_admin", False))(view_func))


# ---------------- CATEGORY ----------------
@admin_required
def category_list_page(request):
    categories = Category.objects.filter(is_deleted=False)
    return render(request, "products/category_list.html", {"categories": categories})


@admin_required
def category_create_page(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("category_list_page")
    else:
        form = CategoryForm()
    return render(request, "products/category_form.html", {"form": form, "title": "Add Category"})


@admin_required
def category_edit_page(request, pk):
    category = get_object_or_404(Category, id=pk, is_deleted=False)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("category_list_page")
    else:
        form = CategoryForm(instance=category)
    return render(request, "products/category_form.html", {"form": form, "title": "Edit Category"})


@admin_required
def category_delete_page(request, pk):
    category = get_object_or_404(Category, id=pk, is_deleted=False)
    category.is_deleted = True
    category.save(update_fields=["is_deleted"])
    messages.success(request, "Category deleted successfully.")
    return redirect("category_list_page")


# ---------------- PRODUCT ----------------
@admin_required
def product_admin_list_page(request):
    products = Product.objects.filter(is_deleted=False)
    return render(request, "products/product_admin_list.html", {"products": products})


@admin_required
def product_create_page(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product added successfully!")
            return redirect("product_admin_list_page")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "title": "Add Product"})


@admin_required
def product_edit_page(request, pk):
    product = get_object_or_404(Product, id=pk, is_deleted=False)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_admin_list_page")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form, "title": "Edit Product"})


@admin_required
def product_delete_page(request, pk):
    product = get_object_or_404(Product, id=pk, is_deleted=False)
    product.is_deleted = True
    product.save(update_fields=["is_deleted"])
    messages.success(request, "Product deleted successfully.")
    return redirect("product_admin_list_page")
