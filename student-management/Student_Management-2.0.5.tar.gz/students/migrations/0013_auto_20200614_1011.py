# Generated by Django 2.1.5 on 2020-06-14 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_fees_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fees_update',
            name='course',
        ),
        migrations.RemoveField(
            model_name='fees_update',
            name='fees_update',
        ),
        migrations.RemoveField(
            model_name='fees_update',
            name='name_of_month',
        ),
    ]
