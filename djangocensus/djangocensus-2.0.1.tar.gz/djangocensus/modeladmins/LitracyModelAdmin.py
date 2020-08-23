from django.contrib.admin import ModelAdmin
from django.db import models
from django import forms


# Your ModelAdmin goes here.
class LitracyModelAdmin(ModelAdmin):
    list_display        = ["content_type", "object_id", "content_object", "status", "author"]
    list_filter         = ["status", "created_at", "updated_at"]
    search_fields       = ["content_object", "content_type", "object_id"]
    formfield_overrides = {
        models.PositiveIntegerField: {"widget": forms.NumberInput(attrs={'size': '18'})},
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
            "fields": [("litracy_male", "litracy_female"), "litracy"]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": ["author", "status"]
        })
    )
