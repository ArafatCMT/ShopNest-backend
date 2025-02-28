from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
import string
import random

def generate_random_string(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # প্রথমবার slug সেট করা
            self.slug = slugify(self.name)

        original_slug = self.slug
        counter = 1

        # ইউনিক slug নিশ্চিত করা
        while Category.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{generate_random_string()}"
            counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
# def slug_generator(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = "SLUG"

# pre_save.connect(slug_generator,sender=Category)