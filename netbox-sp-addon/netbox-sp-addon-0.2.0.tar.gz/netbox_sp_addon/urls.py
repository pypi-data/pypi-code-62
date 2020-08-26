from django.urls import path

from .views import SPDeviceListView

# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (path("devices/", SPDeviceListView.as_view(), name="sp_device_list"),)
