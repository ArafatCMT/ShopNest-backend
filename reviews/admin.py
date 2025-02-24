from django.contrib import admin
from . import models
# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']

    def product(self, obj):
        return obj.product.name
    
    def customer(self, obj):
        return obj.customer.user.username
    
admin.site.register(models.Review, ReviewAdmin)
