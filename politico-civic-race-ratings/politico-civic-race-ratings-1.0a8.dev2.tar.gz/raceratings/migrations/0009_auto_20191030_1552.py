# Generated by Django 2.2.6 on 2019-10-30 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raceratings', '0008_auto_20191021_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='racerating',
            options={'ordering': ('-created', 'pk')},
        ),
    ]
