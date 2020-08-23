from django.db import models
from django.contrib.auth.models import User
from djangocensus.models import ContinentModel
from djangocensus.models.ReligiousPopulationModel import ReligiousPopulationModel
from djangocensus.models.PopulationModel import PopulationModel
from djangocensus.models.LitracyModel import LitracyModel


# Create your models here.
class CountryModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))

    name               = models.CharField(max_length=13)
    slug               = models.SlugField(max_length=13)
    serial             = models.PositiveIntegerField()
    area_sqkm          = models.PositiveIntegerField()
    area_sqmi          = models.PositiveIntegerField()
    continent          = models.ForeignKey(ContinentModel, on_delete=models.CASCADE)
    population         = models.ManyToManyField(PopulationModel, blank=True)
    religious          = models.ManyToManyField(ReligiousPopulationModel, blank=True)
    litracy            = models.ManyToManyField(LitracyModel, blank=True)
    capital            = models.CharField(max_length=50)
    national_language  = models.CharField(max_length=50)
    currency           = models.CharField(max_length=50)
    demonym            = models.CharField(max_length=45)
    author             = models.ForeignKey(User, on_delete=models.CASCADE)
    status             = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['serial']
