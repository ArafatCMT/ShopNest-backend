from django.contrib import admin
from .models import Cart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'category', 'product', 'quantity', 'total_price', 'created_at']

    def customer(self, obj):
        return f"{obj.customer.user.first_name} {obj.customer.user.last_name}"
    
    def category(self, obj):
        return obj.product.category.name 
    
admin.site.register(Cart, CartAdmin)
