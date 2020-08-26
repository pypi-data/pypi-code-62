from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


# Declare a list of menu items to be added to NetBox's built-in naivgation menu
menu_items = (
    PluginMenuItem(
        link="plugins:netbox_sp_addon:sp_device_list",
        link_text="Devices (additional filters)",
    ),
)
