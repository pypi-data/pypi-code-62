from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.admin import ModelAdmin


class VillageModelAdmin(ModelAdmin):
    list_display         = ["name", "pk", "author", "status", "created_at", "updated_at"]
    list_filter          = ["status"]
    search_fields        = ["name", "slug", "author"]
    prepopulated_fields  = {"slug": ("name",)}
    formfield_overrides  = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={'size':'15'})},
        models.FloatField: {'widget': forms.NumberInput(attrs={'size': '15'})}
    }
    fieldsets            = (
        ("Basic Information", {
            "classes": ["extrapretty"],
            "fields": ["serial", ("name", "slug")]
        }),
        ("Geographical Information", {
            "classes": ["collapse", "extrapretty"],
            "fields": [("area_sqkm", "area_sqmi"), ('continent', 'country', 'state', 'district')]
        }),
        ("Demographical Information", {
            "classes": ["collapse", "extrapretty"],
            "fields": ["litracy", "population", "religious"]
        }),
        ("Political Information", {
            "classes": ["collapse", "extrapretty"],
            "fields": ["demonym"]
        }),
        ("Status", {
            "classes": ["extrapretty"],
            "fields": ["author", "status"]
        })
    )
