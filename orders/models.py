from django.db import models
from users.models import User
from products.models import Product

# Create your models here.

class OrderItemQuerySet(models.QuerySet):
     def totalPrice(self):
        return sum(cart.product_price() for cart in self)
    
     def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(null=True, blank=True)
    payment_on_get = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="In processing", verbose_name="Order status")
    
    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        
    def __str__(self) -> str:
        return f"Order #{self.pk} | Customer {self.user.first_name} {self.user.last_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "order_item"
        verbose_name = "Solded product"
        verbose_name_plural = "Solded products"
        
    objects = OrderItemQuerySet.as_manager()