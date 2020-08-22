# Generated by Django 2.0 on 2018-01-25 17:42

from django.db import migrations


def forwards(apps, schema_editor):
    """
    Copy the ClassicalWork and DancePiece data to use the new through models.
    """
    Event = apps.get_model("spectator_events", "Event")
    ClassicalWorkSelection = apps.get_model(
        "spectator_events", "ClassicalWorkSelection"
    )
    DancePieceSelection = apps.get_model("spectator_events", "DancePieceSelection")

    for event in Event.objects.all():

        for work in event.classicalworks.all():
            selection = ClassicalWorkSelection(classical_work=work, event=event)
            selection.save()

        for piece in event.dancepieces.all():
            selection = DancePieceSelection(dance_piece=piece, event=event)
            selection.save()


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0012_add_classical_and_dance_through_models"),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
