from rest_framework import serializers
from products import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'discription', 'product_img_url', 'category', 'brand', 'color', 'quantity', 'sold_quantity', 'price']
        read_only_fields = ['sold_quantity']

    def validate(self, data):
        # Ensure 'sold_quantity' is not being updated
        if 'sold_quantity' in data:
            raise serializers.ValidationError("You cannot update sold_quantity.")
        return data
