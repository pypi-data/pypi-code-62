from osiris.Osiris import Osiris
# import pytest

SYSTEM_NAME = "hydda_test"
PLUGIN_NAME = "openstack"

osiris = Osiris(SYSTEM_NAME, PLUGIN_NAME)

osiris.objectIntrospect("flavor")


def testSelect():
    """
    Unit tests for objectSelect(..)
    """
    assert osiris.objectUnselect("flavor", "7 8 9") == 3
