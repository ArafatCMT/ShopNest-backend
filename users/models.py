from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

GENDER = [
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.CharField(max_length=300, default='https://ibb.co.com/HT3zQNXm')
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True, default='Male')
    join_dated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class UsedToken(models.Model):
    token = models.TextField(unique=True)
    used_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.token}'