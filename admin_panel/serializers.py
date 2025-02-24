from rest_framework import serializers
from . import models

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser', 'is_admin']
        read_only_fields = ['is_staff', 'is_superuser', 'is_admin']