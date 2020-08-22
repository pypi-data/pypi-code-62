# Generated by Django 2.0 on 2018-01-29 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0021_auto_20180129_1735"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="spectator_events.Venue",
            ),
        ),
    ]
