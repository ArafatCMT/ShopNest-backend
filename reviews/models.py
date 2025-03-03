from django.db import models
from products.models import Product
from users.models import Customer
from django.utils import timezone
from decimal import Decimal

RATINGS = [
    (1.0, 1.0),
    (1.5, 1.5),
    (2.0, 2.0),
    (2.5, 2.5),
    (3.0, 3.0),
    (3.5, 3.5),
    (4.0, 4.0),
    (4.5, 4.5),
    (5.0, 5.0)
]

# Create your models here.
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='reviews', on_delete=models.CASCADE)
    rating = models.DecimalField(decimal_places=1, max_digits=3, choices=RATINGS, default=Decimal("0.0"))
    comment = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  # Default ordering to show latest review first

    def __str__(self):
        return f"{self.product}"
