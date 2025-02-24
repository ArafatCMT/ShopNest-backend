from django.db import models
from users.models import Customer
from django.utils import timezone
# Create your models here.

NOTIFICATIONS_STATUS = [
        ('Order Update', 'Order Update'),
        ('Delivery Update', 'Delivery Update'),
]

class Notificaiton(models.Model):
    customer = models.ForeignKey(Customer, related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=300)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATIONS_STATUS, default='Order Update')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  # Default ordering to show latest notifications first

    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}"
