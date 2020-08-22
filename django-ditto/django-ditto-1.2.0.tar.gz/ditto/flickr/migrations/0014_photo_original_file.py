# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 16:09
from __future__ import unicode_literals

import ditto.flickr.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flickr", "0013_photoset_photos_raw"),
    ]

    operations = [
        migrations.AddField(
            model_name="photo",
            name="original_file",
            field=models.FileField(
                blank=True, null=True, upload_to=ditto.flickr.models.Photo.upload_path
            ),
        ),
    ]
