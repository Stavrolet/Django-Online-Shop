from django.db import models
from users.models import User
from products.models import Product

# Create your models here.

class CartQuerySet(models.QuerySet):
    def totalPrice(self):
        return sum(cart.product_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        
    objects = CartQuerySet().as_manager()
    
    text = "No user"
    def __str__(self) -> str:
        return f"Cart {self.user.username if self.user else self.text} | Product {self.product.name} | Quantity {self.quantity}"
    
    def product_price(self) -> int:
        return self.product.price