from dcim.forms import DeviceFilterForm
from dcim.models import RackRole
from utilities.forms import DynamicModelMultipleChoiceField, APISelectMultiple


class SPDeviceFilterForm(DeviceFilterForm):
    field_order = [
        "q",
        "region",
        "site",
        "rack_group_id",
        "rack_role",
        "rack_id",
        "status",
        "role",
        "tenant_group",
        "tenant",
        "manufacturer_id",
        "device_type_id",
        "mac_address",
        "has_primary_ip",
    ]

    rack_role = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(), required=False, label="Rack role",
    )
