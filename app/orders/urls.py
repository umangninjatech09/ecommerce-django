from django.urls import path
from .views import checkout_page, order_list_page, order_detail_page, order_success_page

urlpatterns = [
    path("checkout/", checkout_page, name="checkout_page"),
    # path("buy-now/<int:product_id>/", buy_now, name="buy_now"),
    path("orders/", order_list_page, name="order_list_page"),
    path("order/<int:order_id>/", order_detail_page, name="order_detail_page"),
    path("success/<str:order_no>/", order_success_page, name="order_success_page"),
]
