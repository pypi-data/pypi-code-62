from osiris.Osiris import Osiris

SYSTEM_NAME = "hydda"
PLUGIN_NAME = "openstack"

osiris = Osiris(SYSTEM_NAME, PLUGIN_NAME)

print(osiris.objectUnselect("flavoor", "2333"))
# print(osiris.objectUnselect("flavor"))
