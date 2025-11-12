from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.products'  # ✅ must include 'app.' prefix
    label = 'products'
