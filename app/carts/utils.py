from app.carts.models import Cart

def get_user_cart(request):
    # Logged-in user
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # Guest user using session
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def cart_count(request):
    if request.user.is_authenticated:
        cart = get_user_cart(request)
        count = cart.items.filter(is_deleted=False).count()
        return {"cart_count": count}
    return {"cart_count": 0}