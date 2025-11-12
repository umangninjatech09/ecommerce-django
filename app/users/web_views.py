from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, AddressForm
from .models import Address



@login_required
def home_page(request):
    return render(request, "home.html")


# ---------------------------
# Register
# ---------------------------
def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login_page")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


# ---------------------------
# Login
# ---------------------------
def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username} 👋")
                return redirect("home_page")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


# ---------------------------
# Logout
# ---------------------------
@login_required
def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login_page")


# ---------------------------
# Profile Page
# ---------------------------
@login_required
def profile_page(request):
    return render(request, "users/profile.html", {"user": request.user})


# ---------------------------
# Address List
# ---------------------------
@login_required
def address_list_page(request):
    addresses = request.user.addresses.filter(is_deleted=False)
    return render(request, "users/address_list.html", {"addresses": addresses})


# ---------------------------
# Add Address
# ---------------------------
@login_required
def address_create_page(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Address added successfully.")
            return redirect("address_list_page")
    else:
        form = AddressForm()
    return render(request, "users/address_form.html", {"form": form, "title": "Add Address"})


# ---------------------------
# Edit Address
# ---------------------------
@login_required
def address_edit_page(request, pk):
    address = get_object_or_404(Address, id=pk, user=request.user, is_deleted=False)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("address_list_page")
    else:
        form = AddressForm(instance=address)
    return render(request, "users/address_form.html", {"form": form, "title": "Edit Address"})


# ---------------------------
# Delete (Soft Delete)
# ---------------------------
@login_required
def address_delete_page(request, pk):
    address = get_object_or_404(Address, id=pk, user=request.user, is_deleted=False)
    address.is_deleted = True
    address.save(update_fields=["is_deleted"])
    messages.success(request, "Address deleted successfully.")
    return redirect("address_list_page")
