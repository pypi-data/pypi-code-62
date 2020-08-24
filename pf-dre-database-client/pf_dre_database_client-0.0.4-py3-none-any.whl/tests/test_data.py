from unittest import TestCase

from mms.util import helpers

class TestData(TestCase):
    def setUp(self):
        self.clientArgs = helpers.get_db_client_kwargs()
