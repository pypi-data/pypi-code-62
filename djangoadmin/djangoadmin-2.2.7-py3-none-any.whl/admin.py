from django.contrib import admin
from djangoadmin.models import UserModel
from djangoadmin.modeladmins import UserModelAdmin


# Register all the models here.
admin.site.register(UserModel, UserModelAdmin)