from django.contrib import admin
from .models import Admin
# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'is_staff', 'is_superuser', 'is_admin']

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def username(self, obj):
        return obj.user.username
    
    def email(self, obj):
        return obj.user.email
    
    def is_superuser(self, obj):
        return obj.user.is_superuser
    
    def is_staff(self, obj):
        return obj.user.is_staff

admin.site.register( Admin, ModelAdmin)
