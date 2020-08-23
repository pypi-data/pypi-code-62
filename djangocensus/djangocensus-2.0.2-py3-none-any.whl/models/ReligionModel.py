from django.db import models
from django.contrib.auth.models import User


# Your models goes here.
class ReligionModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))

    name       = models.CharField(max_length=15)
    slug       = models.SlugField(max_length=15)
    serial     = models.PositiveIntegerField()
    content    = models.TextField()
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    status     = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Religion"
        verbose_name_plural = "Religions"
        ordering = ['serial']
