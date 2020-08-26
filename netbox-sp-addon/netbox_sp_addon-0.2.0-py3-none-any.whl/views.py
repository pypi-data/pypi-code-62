from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from dcim.views import DeviceListView

from .filters import SPDeviceFilterSet
from .forms import SPDeviceFilterForm


class SPDeviceListView(DeviceListView):
    filterset = SPDeviceFilterSet
    filterset_form = SPDeviceFilterForm
