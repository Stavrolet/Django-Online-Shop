from django.contrib import admin
from products.models import Category, Product

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    list_display = ("name",)

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    list_display = ("name", "quantity", "price", "discount")
    list_editable = ("discount",)
    search_fields = ("name", "discription")
    list_filter = ("discount", "quantity", "category")
    
    fields = (
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity"
    )