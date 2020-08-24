import json
from unittest import TestCase
from decouple import config

from srvmsdk.app.client import get_client


class Test(TestCase):

    def setUp(self) -> None:
        self.secret_id = config('S_ID', default=None)
        self.secret_key = config('S_KEY', default=None)
        self.region = config('REGION', default=None)

    def test_get_client(self):
        tencent = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)
        res = tencent.DescribeZones()

        self.assertEqual(res.get('code'), 0)
        # self.fail()
