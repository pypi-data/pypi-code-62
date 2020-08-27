
from django.db import migrations, models
from django.core.management import call_command

from ..apps import APP_NAME


def load_initial_data(apps, schema_editor):
    # get the correct versions of models using the app registry
    Country = apps.get_model(APP_NAME, "Country")
    Region = apps.get_model(APP_NAME, "Region")

    call_command('loaddata', 'initial_data.json', app_label=APP_NAME)

## logic for migrating backwards
def reverse_func(apps, schema_editor):
    Country = apps.get_model(APP_NAME, "Country")
    Region = apps.get_model(APP_NAME, "Region")

    Country.objects.all().delete()
    Region.objects.all().delete()

class Migration(migrations.Migration):
    # Django automatically adds dependencies for your migration
    # when you generate the empty migration
    dependencies = [
        (APP_NAME, '0001_initial'),
    ]

    # the RunPython operation with the two callables passed in
    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]