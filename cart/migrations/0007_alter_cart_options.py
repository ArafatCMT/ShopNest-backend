# Generated by Django 5.1.6 on 2025-03-10 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cart_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-created_at']},
        ),
    ]
