from django.contrib import admin
from .models import Order,OrderHistory
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'payment_status', 'order_status', 'created_at', 'is_delivered']

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total_amount', 'payment_status', 'order_status',  'is_delivered', 'created_at']

    def order_id(self, obj):
        return obj.order.id
    
    def total_amount(self, obj):
        return obj.order.total_amount
    
    def payment_status(self, obj):
        return obj.order.payment_status
    
    def order_status(self, obj):
        return obj.order.order_status
    
    def is_delivered(self, obj):
        return obj.order.is_delivered
    

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)

