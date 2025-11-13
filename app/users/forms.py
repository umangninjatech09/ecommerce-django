from typing import Any
from django import forms
from .models import User, Address


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_customer = True
        user.is_retailer = False
        user.is_admin = False
        if commit:
            user.save()
        return user
    

class RetailerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "phone_number"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_customer = False
        user.is_retailer = True   # Retailer role
        if commit:
            user.save()
        return user
    
    

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "receiver_name",
            "phone",
            "address_line",
            "city",
            "state",
            "country",
            "postal_code",
            "is_default",
        ]
