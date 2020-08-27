from django.db import models
from django.utils.translation import ugettext_lazy as _

import autoslug

# Create your models here.
APP_NAME = "country_regions"


CONTINENT_CHOICES = (
    ('OC', _('Oceania')),
    ('EU', _('Europe')),
    ('AF', _('Africa')),
    ('NA', _('North America')),
    ('AN', _('Antarctica')),
    ('SA', _('South America')),
    ('AS', _('Asia')),
)

class Base(models.Model):
    """
    Base model with boilerplate for all models.
    """

    name = models.CharField(max_length=200, db_index=True)
    name_ascii = models.CharField(max_length=200, blank=True, db_index=True)
    slug = autoslug.AutoSlugField(populate_from='name_ascii')
    geoname_id = models.IntegerField(null=True, blank=True, unique=True)
    alternate_names = models.TextField(null=True, blank=True, default='')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        display_name = getattr(self, 'display_name', None)
        if display_name:
            return display_name
        return self.name


class Country(Base):
    """
    Base Country model.
    """

    code2 = models.CharField(max_length=2, null=True, blank=True, unique=True)
    code3 = models.CharField(max_length=3, null=True, blank=True, unique=True)
    continent = models.CharField(max_length=2, db_index=True,
                                 choices=CONTINENT_CHOICES)
    tld = models.CharField(max_length=5, blank=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta(Base.Meta):
        verbose_name_plural = _('countries')


class Region(Base):
    """
    Base Region/State model.
    """

    display_name = models.CharField(max_length=200)
    geoname_code = models.CharField(max_length=50, null=True, blank=True,
                                    db_index=True)

    country = models.ForeignKey(APP_NAME + '.Country',
                                on_delete=models.CASCADE)

    class Meta(Base.Meta):
        unique_together = (('country', 'name'), ('country', 'slug'))
        verbose_name = _('region/state')
        verbose_name_plural = _('regions/states')

    def get_display_name(self):
        return '%s, %s' % (self.name, self.country.name)