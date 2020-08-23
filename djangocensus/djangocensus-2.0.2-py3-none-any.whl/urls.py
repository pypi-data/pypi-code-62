from django.conf.urls import re_path, include

app_name = 'djangocensus'

# Your urlpatterns goes here.
urlpatterns = [
    re_path(r'^api/', include("djangocensus.rest_api.urls")),
]