from django.db import models
from app.users.models import User
from app.core.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"
    

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart of {self.cart.user.username if self.cart.user else 'Anonymous'}"
    
    @property
    def total_price(self):
        return self.quantity * self.price
    
    