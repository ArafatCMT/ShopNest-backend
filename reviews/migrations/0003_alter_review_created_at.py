# Generated by Django 5.1.6 on 2025-02-21 17:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_rename_create_at_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
