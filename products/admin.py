from django.contrib import admin
from products.models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'brand', 'category', 'price', 'quantity', 'sold_quantity' ]

admin.site.register(Product, ProductAdmin)
