# Generated by Django 2.0 on 2018-02-08 11:45

from django.db import migrations


def forwards(apps, schema_editor):
    """
    Change all DancePiece objects into Work objects, and their associated
    data into WorkRole and WorkSelection models, then delete the DancePiece.
    """
    DancePiece = apps.get_model("spectator_events", "DancePiece")
    Work = apps.get_model("spectator_events", "Work")
    WorkRole = apps.get_model("spectator_events", "WorkRole")
    WorkSelection = apps.get_model("spectator_events", "WorkSelection")

    for dp in DancePiece.objects.all():

        work = Work.objects.create(
            kind="dancepiece", title=dp.title, title_sort=dp.title_sort
        )

        for role in dp.roles.all():
            WorkRole.objects.create(
                creator=role.creator,
                work=work,
                role_name=role.role_name,
                role_order=role.role_order,
            )

        for selection in dp.events.all():
            WorkSelection.objects.create(
                event=selection.event, work=work, order=selection.order
            )

        dp.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0027_classicalworks_to_works"),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
