# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-01 09:57
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import forkilla.models


class Migration(migrations.Migration):

    dependencies = [
        ('forkilla', '0005_review_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='featured_photo',
            field=models.ImageField(upload_to=forkilla.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_promot',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
    ]
