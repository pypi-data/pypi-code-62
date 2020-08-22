from django.db import models
from django.contrib.auth.models import User


class UserModel(models.Model):
    STATUS_CHOICES   = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))
    user             = models.OneToOneField(User, on_delete=models.CASCADE)
    bio              = models.CharField(max_length=30, blank=True, null=True)
    image            = models.ImageField(blank=True, null=True, upload_to="uploads")
    address          = models.CharField(max_length=100, blank=True, null=True)
    phone            = models.BigIntegerField(blank=True, null=True)
    website          = models.URLField(blank=True, null=True)
    verification     = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    is_admin         = models.BooleanField(default=False)
    is_editor        = models.BooleanField(default=False)
    is_writter       = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    status           = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ['pk']
        verbose_name = 'User'
        verbose_name_plural = 'Users'