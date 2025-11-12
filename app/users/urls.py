from django.urls import path
from app.users import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("address/", views.add_address, name="add_address"),
    path("address/<int:address_id>/", views.update_address, name="update_address"),
    path("address/<int:address_id>/delete/", views.delete_address, name="delete_address"),
    path("addresses/", views.list_addresses, name="list_addresses"),
]
