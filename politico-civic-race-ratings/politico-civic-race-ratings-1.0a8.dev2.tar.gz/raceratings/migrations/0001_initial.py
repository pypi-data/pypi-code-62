# Generated by Django 2.0.6 on 2018-07-13 19:42

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import raceratings.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("election", "0001_initial"),
        ("geography", "0002_point_pointlabeloffset"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rating_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BadgeType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=140)),
                ("short_label", models.CharField(max_length=30)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=50)),
                ("short_label", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="DataProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", django.contrib.postgres.fields.jsonb.JSONField()),
                (
                    "division",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geography.Division",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RaceBadge",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "explanation",
                    raceratings.fields.MarkdownField(blank=True, null=True),
                ),
                (
                    "badge_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="raceratings.BadgeType",
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="badges",
                        to="election.Race",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RaceRating",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                (
                    "explanation",
                    raceratings.fields.MarkdownField(blank=True, null=True),
                ),
                ("incumbent", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ratings",
                        to="raceratings.Author",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ratings",
                        to="raceratings.Category",
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="election.Race",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RatingPageContent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("object_id", models.CharField(max_length=500)),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(
                                ("app_label", "election"), ("model", "race")
                            ),
                            models.Q(
                                ("app_label", "raceratings"),
                                ("model", "ratingpagetype"),
                            ),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="raceratings.RatingPageContent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RatingPageContentBlock",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", raceratings.fields.MarkdownField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="RatingPageContentType",
            fields=[
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        editable=False,
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="RatingPageType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "model_type",
                    models.CharField(
                        choices=[("Race", "race"), ("Home", "home")],
                        max_length=4,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ratingpagecontentblock",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="raceratings.RatingPageContentType",
            ),
        ),
        migrations.AddField(
            model_name="ratingpagecontentblock",
            name="page",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blocks",
                to="raceratings.RatingPageContent",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ratingpagecontentblock",
            unique_together={("page", "content_type")},
        ),
    ]
