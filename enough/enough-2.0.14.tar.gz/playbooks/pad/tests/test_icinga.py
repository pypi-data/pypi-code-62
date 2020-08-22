from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'website-host')
        assert r['attrs']['name'] == 'website-host'

    def test_service(self):
        assert self.is_service_ok('website-host!Pad')
