from django.urls import path
from . import web_views

urlpatterns = [
    path("home/", web_views.home_page, name="home_page"),
    path("register/", web_views.register_page, name="register_page"),
    path("login/", web_views.login_page, name="login_page"),
    path("logout/", web_views.logout_page, name="logout_page"),
    path("profile/", web_views.profile_page, name="profile_page"),
    path("addresses/", web_views.address_list_page, name="address_list_page"),
    path("addresses/add/", web_views.address_create_page, name="address_create_page"),
    path("addresses/<int:pk>/edit/", web_views.address_edit_page, name="address_edit_page"),
    path("addresses/<int:pk>/delete/", web_views.address_delete_page, name="address_delete_page"),
    path("forgot-password/", web_views.forgot_password_page, name="forgot_password_page"),
    path("reset-password/<uidb64>/<token>/", web_views.reset_password_page, name="reset_password_page"),
]
