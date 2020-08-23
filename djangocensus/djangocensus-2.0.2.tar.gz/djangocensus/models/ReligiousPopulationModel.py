from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from djangocensus.models.ReligionModel import ReligionModel


# Your model goes here.
class ReligiousPopulationModel(models.Model):
    STATUS_CHOICES = (("ACTIVE", "active"), ("DEACTIVE", "deactive"))

    content_type         = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id            = models.PositiveIntegerField()
    content_object       = GenericForeignKey('content_type', 'object_id')
    serial               = models.PositiveIntegerField()
    religion             = models.ForeignKey(ReligionModel, on_delete=models.CASCADE)
    religious_population = models.BigIntegerField()
    religious_percentage = models.FloatField()
    author               = models.ForeignKey(User, on_delete=models.CASCADE)
    status               = models.CharField(max_length=8, choices=STATUS_CHOICES)
    census_title         = models.CharField(max_length=60)
    census_taken         = models.DateField()
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content_type}: {self.content_object} | Object ID: {self.object_id}"

    class Meta:
        verbose_name = "Religious Population"
        verbose_name_plural = "Religious Populations"
        ordering = ["serial"]
