from django.db import models
from users.models import Customer
from products.models import Product
from django.utils import timezone

SIZES = [
    ('Not Applicable', 'Not Applicable'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

# Create your models here.
class Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, choices=SIZES, default='Not Applicable')
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)

    class Meta:
        # Jodi ekta product cart e already thake, tahole oi product abar notun kore cart e add kora jabe na. Quantity increase hote parbe, kintu notun entry create kora jabe na.
        unique_together = ('customer', 'product') 

    def __str__(self):
        return f"Cart of {self.customer.user.username} - {self.product.name} (Quantity: {self.quantity})"

