from django.db import models
from categories.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    product_img_url = models.CharField(max_length=200, null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=50, default='No Brand')
    color = models.CharField(max_length=50, null=True, blank=True, default='Not Applicable')
    quantity = models.IntegerField(default=0)
    sold_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

    

# https://fabrilife.com/product/71490-mens-premium-blank-t-shirt-maroon