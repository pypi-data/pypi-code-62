from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Your model goes here.
class LitracyModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))

    content_type      = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id         = models.PositiveIntegerField()
    content_object    = GenericForeignKey('content_type', 'object_id')
    serial            = models.PositiveIntegerField()
    litracy_male      = models.BigIntegerField()
    litracy_female    = models.BigIntegerField()
    litracy           = models.BigIntegerField()
    author            = models.ForeignKey(User, on_delete=models.CASCADE)
    status            = models.CharField(max_length=8, choices=STATUS_CHOICES)
    census_title      = models.CharField(max_length=60)
    census_taken      = models.DateField()
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content_type}: {self.content_object} | Object ID: {self.object_id}"

    class Meta:
        verbose_name = "Litracy"
        verbose_name_plural = "Litracies"
        ordering = ["serial"]