from extras.plugins import PluginConfig


class SPAddonConfig(PluginConfig):
    """
    This class defines attributes for the NetBox Animal Sounds plugin.
    """

    # Plugin package name
    name = "netbox_sp_addon"

    # Human-friendly name and description
    verbose_name = "scanplus Addon"
    description = "Add functions used by scanplus GmbH"

    # Plugin version
    version = "0.2.0"

    # Plugin author
    author = "Tobias Genannt"
    author_email = "t.genannt@scanplus.de"

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {}

    # Base URL path. If not set, the plugin name will be used.
    base_url = "sp-addon"

    # Caching config
    caching_config = {}


config = SPAddonConfig
