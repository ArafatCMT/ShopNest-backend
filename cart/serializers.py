from rest_framework import serializers
from . import models

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id', 'customer', 'product', 'quantity', 'size', 'created_at', 'total_price']
        # read_only_fields = ['customer']