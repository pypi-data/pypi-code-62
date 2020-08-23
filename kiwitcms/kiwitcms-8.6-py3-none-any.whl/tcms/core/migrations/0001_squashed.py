# Generated by Django 2.0.7 on 2018-07-25 14:28

from django.db import migrations


def forwards_add_initial_data(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.bulk_create([
        group_model(name='Administrator'),
        group_model(name='Tester'),
    ])

    site_model = apps.get_model('sites', 'Site')
    site_model.objects.create(name='localhost', domain='127.0.0.1:8000')


def reverse_remove_initial_data(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.filter(name__in=['Administrator', 'Tester']).delete()

    site_model = apps.get_model('sites', 'Site')
    site_model.objects.filter(name='localhost').delete()


def forwards_add_default_perms(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    permission_model = apps.get_model('auth', 'Permission')

    admin = group_model.objects.get(name='Administrator')
    all_perms = permission_model.objects.all()
    admin.permissions.add(*all_perms)

    tester = group_model.objects.get(name='Tester')
    # apply all permissions for test case & product management
    for app_name in ['bugs', 'django_comments', 'management', 'linkreference',
                     'testcases', 'testplans', 'testruns']:
        app_perms = permission_model.objects.filter(content_type__app_label__contains=app_name)
        tester.permissions.add(*app_perms)


def reverse_remove_default_perms(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')

    admin = group_model.objects.get(name='Administrator')
    admin.permissions.clear()

    tester = group_model.objects.get(name='Tester')
    tester.permissions.clear()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_add_initial_data,
            reverse_code=reverse_remove_initial_data,
        ),
        migrations.RunPython(
            code=forwards_add_default_perms,
            reverse_code=reverse_remove_default_perms,
        ),
    ]
