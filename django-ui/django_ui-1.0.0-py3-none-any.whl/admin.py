from django.contrib import admin
from django.conf import settings

if hasattr(settings, 'SHOW_APP_EXAMPLE_UI'):
    from django_ui.forms import ModelExampleForm
    from django_ui.models import ModelExample


    class ModelExampleAdmin(admin.ModelAdmin):
        model = ModelExample
        form = ModelExampleForm

        list_display = ('name', 'occupation')


    admin.site.register(ModelExample, ModelExampleAdmin)

if hasattr(settings, 'USE_APP_THEME_UI_ADMIN'):
    from django_ui.models import ThemeUI


    class SettingsUIAdmin(admin.ModelAdmin):
        model = ThemeUI
        list_display = ('name_theme', 'applied', 'site_name', 'title_window',)

        def save_model(self, request, obj, form, change):
            list_settings = ThemeUI.objects.all()
            for setting in list_settings:
                setting.apply = False
                setting.save()

            obj.save()


    admin.site.register(ThemeUI, SettingsUIAdmin)
