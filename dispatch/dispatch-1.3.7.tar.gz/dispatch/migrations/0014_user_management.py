# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 18:00

import dispatch.modules.auth.helpers
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0013_user_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('permissions', models.CharField(default=b'', max_length=255)),
                ('expiration_date', models.DateTimeField(default=dispatch.modules.auth.helpers.get_expiration_date)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invited_person', to='dispatch.Person')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
