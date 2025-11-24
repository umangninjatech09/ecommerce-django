from django.urls import path
from .views import wishlist_page, toggle_wishlist

urlpatterns = [
    path("", wishlist_page, name="wishlist_page"),
    path("toggle/<int:product_id>/", toggle_wishlist, name="toggle_wishlist"),
]
