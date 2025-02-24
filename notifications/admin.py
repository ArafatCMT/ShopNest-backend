from django.contrib import admin
from .models import Notificaiton

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'title', 'message', 'notification_type', 'created_at']

admin.site.register(Notificaiton,NotificationAdmin)
