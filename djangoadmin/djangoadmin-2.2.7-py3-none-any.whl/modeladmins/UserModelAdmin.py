from django import forms
from django.db import models
from django.contrib.admin import ModelAdmin


class UserModelAdmin(ModelAdmin):
    list_display        = ["user", "pk", "verification", "is_administrator", "is_admin", "is_editor", "is_writter", "status"]
    list_filter         = ["created_at", "updated_at", "status", "verification"]
    search_fields       = ["user", "pk"]

    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size':35})},
        models.BigIntegerField: {'widget': forms.NumberInput(attrs={'size': 35})},
        models.URLField: {'widget': forms.URLInput(attrs={'size': 35})}
    }

    fieldsets           = (
        ("Select Object", {
            "classes": ["extrapretty"],
            "fields": ["user"]
        }),
        ("General Information", {
            "classes": ["extrapretty", "collapse"],
            "fields": ["bio", "address", "phone", "website"]
        }),
        ("Multimedia Files", {
            "classes": ["extrapretty", "collapse"],
            "fields": ["image"]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": [("verification", "is_administrator", "is_admin", "is_editor", "is_writter"), "status"]
        })
    )