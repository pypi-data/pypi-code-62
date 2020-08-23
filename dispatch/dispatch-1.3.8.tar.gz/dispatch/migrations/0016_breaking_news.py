# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0015_image_wrap'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='breaking_timeout',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='is_breaking',
            field=models.BooleanField(default=False),
        ),
    ]
