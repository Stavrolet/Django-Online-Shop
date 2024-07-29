from django.contrib import admin
from carts.admin import CartTabularAdmin
from .models import User
from orders.admin import OrderTabularAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = "username", "first_name", "last_name", "email"
    search_fields = "username", "first_name", "last_name", "email"
    
    inlines = (OrderTabularAdmin, CartTabularAdmin)