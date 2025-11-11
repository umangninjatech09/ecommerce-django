from django import forms
from .models import User, Address


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]


class LoginForm(forms.Form):
    username = forms.CharField()
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
