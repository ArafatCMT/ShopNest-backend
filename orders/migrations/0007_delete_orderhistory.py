# Generated by Django 5.1.6 on 2025-03-10 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_options_alter_orderhistory_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
