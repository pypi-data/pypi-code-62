# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-07 06:39


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("perimeter", "0003_auto_20150612_0151")]

    operations = [
        migrations.AlterField(
            model_name="accesstokenuse",
            name="user_email",
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name="Token used by (email)",
            ),
        ),
        migrations.AlterField(
            model_name="accesstokenuse",
            name="user_name",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Token used by (name)",
            ),
        ),
    ]
