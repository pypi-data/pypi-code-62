import django_filters

from dcim.filters import DeviceFilterSet
from dcim.models import RackRole


class SPDeviceFilterSet(DeviceFilterSet):
    rack_role = django_filters.ModelMultipleChoiceFilter(
        queryset=RackRole.objects.all(),
        field_name="rack__role",
        label="Rack role (ID)",
    )
