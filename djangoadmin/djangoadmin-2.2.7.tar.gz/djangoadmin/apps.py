from django.apps import AppConfig


class DjangoadminConfig(AppConfig):
    name = 'djangoadmin'

    def ready(self):
        from djangoadmin import signals