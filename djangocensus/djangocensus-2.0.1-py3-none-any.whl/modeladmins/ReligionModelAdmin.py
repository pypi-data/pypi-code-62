from django.contrib.admin import ModelAdmin
from django.db import models
from django import forms


class ReligionModelAdmin(ModelAdmin):
    list_display        = ["name", "pk", "status", "author"]
    list_filter         = ["status", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields       = ["name", "slug"]
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size': '34'})}
    }
    fieldsets           = (
        ("Basic Information", {
            "classes": ["extrapretty"],
            "fields": [("name", "slug"), "serial"]
        }),
        ("Extra Information", {
            "classes": ["extrapretty", "collapse"],
            "fields": ["content"]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": ["author", "status"]
        })
    )
