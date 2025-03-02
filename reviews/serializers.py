from rest_framework import serializers
from . import models

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'customer', 'product', 'comment', 'rating', 'created_at']
        read_only_fields = ['customer']