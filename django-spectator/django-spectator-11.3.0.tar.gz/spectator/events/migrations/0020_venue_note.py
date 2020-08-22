# Generated by Django 2.0 on 2018-01-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0019_auto_20180127_1653"),
    ]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="note",
            field=models.TextField(
                blank=True,
                help_text="Optional. Paragraphs will be surrounded with &lt;p&gt;&lt;/p&gt; tags. HTML allowed.",  # noqa: E501
            ),
        ),
    ]
