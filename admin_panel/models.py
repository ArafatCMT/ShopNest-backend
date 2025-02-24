from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.CharField(max_length=250, null=True, blank=True, default='https://ibb.co.com/TqMgm73P')
    is_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
