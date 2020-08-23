# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-07 04:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0002_person_social_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='preview_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
