# Generated by Django 5.1.6 on 2025-02-25 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cart_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='size',
        ),
    ]
