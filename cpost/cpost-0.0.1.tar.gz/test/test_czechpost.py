
from datetime import datetime
import unittest

import cpost


class TestCzechPost(unittest.TestCase):
    def test_regions(self):
        x = cpost.regions()
    def test_districts(self):
        x = cpost.districts(11)
    def test_cities(self):
        x = cpost.cities(55)
    def test_city_parts(self):
        x = cpost.city_parts(5185)
    def test_streets(self):
        x = cpost.streets(12501)
    def test_addresses(self):
        x = cpost.addresses(28783)

__all__ = ["TestCzechPost"]
        