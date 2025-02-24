from rest_framework import serializers
from products import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'discription', 'product_img_url', 'category', 'brand', 'color', 'quantity', 'sold_quantity', 'price']
        read_only_fields = ['sold_quantity']
