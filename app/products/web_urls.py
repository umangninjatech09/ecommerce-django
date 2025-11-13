from django.urls import path
from . import web_views

urlpatterns = [
    path("", web_views.home_page, name="home_page"),
]
