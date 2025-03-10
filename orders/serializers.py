from rest_framework import serializers
from orders import models

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'customer', 'product', 'total_amount', 'payment_status', 'order_status', 'created_at', 'is_delivered']
        # read_only_fields = ['total_amount']
        # read_only_fields = ['customer']

# class OrderHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.OrderHistory
#         fields = '__all__'