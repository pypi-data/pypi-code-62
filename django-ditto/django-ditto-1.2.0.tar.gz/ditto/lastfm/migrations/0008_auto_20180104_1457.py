# Generated by Django 2.0 on 2018-01-04 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lastfm", "0007_set_post_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scrobble",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="scrobbles",
                to="lastfm.Album",
            ),
        ),
    ]
