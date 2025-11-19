from django.urls import path
from . import views, web_views

urlpatterns = [
    # API endpoints
    path("products/", views.product_list, name="product_list_api"),
    # path("products/<slug:slug>/", views.product_detail, name="product_detail_api"),

    # Web pages
    path("category/<slug:slug>/", web_views.product_list_page, name="product_list"),
    path("product/<slug:slug>/", web_views.product_detail_page, name="product_detail"),
    path("category/<slug:category_slug>/", web_views.product_list_page, name="product_list"),
    path("search/", web_views.product_search, name="product_search"),
    path("products/category/<slug:slug>/", web_views.product_list_page, name="product_list"),
    path("products/", web_views.product_list_page, name="all_products"),
]
