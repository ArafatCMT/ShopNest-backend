# Generated by Django 5.1.6 on 2025-02-22 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0004_product_size'),
        ('users', '0002_alter_customer_join_dated'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('customer', 'product')},
        ),
    ]
