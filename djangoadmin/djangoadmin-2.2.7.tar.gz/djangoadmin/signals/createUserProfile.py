from django.db.models.signals import post_save
from django.contrib.auth.models import User
from djangoadmin.models.UserModel import UserModel
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserModel.objects.create(user=instance)