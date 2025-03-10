from django.db import models
from users.models import Customer
from products.models import Product
from django.utils import timezone


PAYMENT_STATUS = [
    ('Unpaid', 'Unpaid'),
    ('Paid', 'Paid'),
]
ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
]

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Unpaid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Default ordering to show latest order first


    def __str__(self):
        return f"Order {self.id} - {self.customer.user.first_name} {self.customer.user.last_name}"
    

# class OrderHistory(models.Model):
#     customer = models.ForeignKey(Customer, related_name='order_history', on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, related_name='order_history', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-created_at']  # Default ordering to show latest order first

#     def __str__(self):
#         return f"Order #{self.order.id} placed by {self.customer.user.first_name} {self.customer.user.last_name}"
