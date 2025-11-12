from django.urls import path
from . import admin_views

urlpatterns = [
    # Category Admin
    path("categories/", admin_views.category_list_page, name="category_list_page"),
    path("categories/add/", admin_views.category_create_page, name="category_add_page"),
    path("categories/<int:pk>/edit/", admin_views.category_edit_page, name="category_edit_page"),
    path("categories/<int:pk>/delete/", admin_views.category_delete_page, name="category_delete_page"),

    # Product Admin
    path("products/", admin_views.product_admin_list_page, name="product_admin_list_page"),
    path("products/add/", admin_views.product_create_page, name="product_add_page"),
    path("products/<int:pk>/edit/", admin_views.product_edit_page, name="product_edit_page"),
    path("products/<int:pk>/delete/", admin_views.product_delete_page, name="product_delete_page"),
]
