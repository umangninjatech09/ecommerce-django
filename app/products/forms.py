from django import forms
from .models import Product, Category, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "category-slug"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Category description"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "description", "price", "discount_price", "stock", "thumbnail", "is_active"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product Name"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "product-slug"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Product description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
            "discount_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Discounted Price"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Stock quantity"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
