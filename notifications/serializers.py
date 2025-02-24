from rest_framework import serializers
from. models import notifications

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notifications
        fields = ['id', 'customer', 'title', 'message', 'notification_type', 'created_at']