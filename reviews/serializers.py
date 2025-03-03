from rest_framework import serializers
from . import models
from decimal import Decimal

class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    class Meta:
        model = models.Review
        fields = ['id', 'customer', 'product', 'comment', 'rating', 'created_at']
        read_only_fields = ['customer']

    def validate_rating(self, value):
        # print("Received Type:", type(value))  # Debugging line
        # print("Received Value:", value)
    
        return value  # If already Decimal