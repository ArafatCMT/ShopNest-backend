from django.contrib import admin
from users.models import Customer, UsedToken

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'phone_number', 'address', 'gender', 'join_dated', 'is_verified']

    def full_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def username(self, obj):
        return obj.user.username
    
    def is_verified(self, obj):
        return obj.user.is_active


admin.site.register(Customer,CustomerAdmin)
admin.site.register(UsedToken)
