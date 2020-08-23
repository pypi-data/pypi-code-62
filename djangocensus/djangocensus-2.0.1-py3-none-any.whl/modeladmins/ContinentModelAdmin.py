from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.admin import ModelAdmin


class ContinentModelAdmin(ModelAdmin):
    list_display         = ["name", "pk", "author", "status", "created_at", "updated_at"]
    list_filter          = ["status"]
    search_fields        = ["name", "slug", "author"]
    prepopulated_fields  = {"slug": ("name",)}
    formfield_overrides  = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size':'15'})},
    }
    fieldsets            = (
        ("Basic Information", {
            "classes": ["extrapretty"],
            "fields": ["serial", ("name", "slug")]
        }),
        ("Geographical Information", {
            "classes": ["collapse", "extrapretty"],
            "fields": [("area_sqkm", "area_sqmi")]
        }),
        ("Demographical Information", {
            "classes": ["collapse", "extrapretty"],
            "fields": ["number_of_countries", "demonym", "litracy", "population", "religious"]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": ["author", "status"]
        })
    )
