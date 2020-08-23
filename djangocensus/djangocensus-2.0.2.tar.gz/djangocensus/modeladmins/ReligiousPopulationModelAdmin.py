from django.contrib.admin import ModelAdmin
from django.db import models
from django import forms


# your modeladmin goes here.
class ReligiousPopulationModelAdmin(ModelAdmin):
    list_display        = ["content_object", "object_id", "status", "author"]
    list_filter         = ["status", "created_at", "updated_at"]
    search_fields       = ["content_object"]
    formfield_overrides = {
        models.PositiveIntegerField: {"widget": forms.NumberInput(attrs={'size': '15'})},
        models.FloatField: {"widget": forms.NumberInput(attrs={'size': '15'})},
        models.BigIntegerField: {"widget": forms.NumberInput(attrs={'size': '18'})}
    }
    fieldsets           = (
        ("Census Information", {
            "classes": ["extrapretty"],
            "fields": ["census_title", "census_taken"]
        }),
        ("Instance for", {
            "classes": ["extrapretty"],
            "fields": [("content_type", "object_id"), "serial"]
        }),
        ("Data", {
            "classes": ["extrapretty"],
            "fields": ["religion", ("religious_population", "religious_percentage")]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": ["author", "status"]
        })
    )