# Generated by Django 5.1.6 on 2025-02-21 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='join_dated',
            field=models.DateField(auto_now_add=True),
        ),
    ]
