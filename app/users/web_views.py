from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, AddressForm, RetailerRegisterForm
from .models import Address
from app.products.models import Product, Category
from django.db.models import Sum
from django.apps import apps
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


User = apps.get_model("users", "User")

token_generator = PasswordResetTokenGenerator()


def home_page(request):
    categories = Category.objects.filter(is_deleted=False)
    category_data = []

    for category in categories:
        products = Product.objects.filter(
            category=category, 
            is_active=True, 
            is_deleted=False
        )[:6]

        category_data.append({
            "category": category,
            "products": products
        })

    return render(request, "home.html", {"category_data": category_data})

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


def retailer_register_page(request):
    if request.method == "POST":
        form = RetailerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Retailer account created. Please login.")
            return redirect("login_page")
    else:
        form = RetailerRegisterForm()
    return render(request, "users/retailer_register.html", {"form": form})


def forgot_password_page(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("forgot_password_page")

        # Generate reset link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain

        reset_link = f"http://{domain}/user/reset-password/{uid}/{token}/"

        # Email message
        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=None,
            recipient_list=[email]
        )

        messages.success(request, "Password reset link sent to your email.")
        return redirect("login_page")

    return render(request, "users/forgot_password.html")



def reset_password_page(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully. Please login.")
            return redirect("login_page")
        return render(request, "users/reset_password.html")
    else:
        messages.error(request, "Invalid password reset link.")
        return redirect("login_page")


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

            if user:
                login(request, user)

                # REDIRECT BASED ON ROLE
                if user.is_retailer or user.is_admin:
                    return redirect("product_admin_list_page")  # Retailer dashboard
                else:
                    return redirect("home_page")  # Customer home page
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
# @login_required
# def profile_page(request):
#     orders = request.user.orders.order_by("-created_at")
#     return render(request, "users/profile.html", {
#         "user": request.user,
#         "orders": orders
#     })

@login_required
def profile_page(request):
    # fetch user orders
    orders = request.user.orders.order_by("-created_at")

    # basic stats
    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum("total_amount"))["total"] or 0

    # recent orders for quick view
    recent_orders = orders[:5]

    # try to compute retailer product count if product model has an owner field
    products_count = None
    if getattr(request.user, "is_retailer", False):
        try:
            Product = apps.get_model("products", "Product")
            # attempt a common ownership field; try multiple possibilities
            # this will fail silently if fields don't exist
            try:
                products_count = Product.objects.filter(created_by=request.user, is_deleted=False).count()
            except Exception:
                try:
                    products_count = Product.objects.filter(seller=request.user, is_deleted=False).count()
                except Exception:
                    # can't determine seller relationship — set None
                    products_count = None
        except LookupError:
            products_count = None

    context = {
        "user": request.user,
        "orders": orders,
        "total_orders": total_orders,
        "total_spent": total_spent,
        "recent_orders": recent_orders,
        "products_count": products_count,
    }
    return render(request, "users/profile.html", context)


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
