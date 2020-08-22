
import os
import pickle
import re
import unittest

import eurostat_deaths as eurostat

class TestPopulations(unittest.TestCase):
    def test_populations_output(self):
        data = eurostat.populations(chunksize = 10)
        # columns
        self.assertIn("sex", data.columns)
        self.assertIn("age", data.columns)
        self.assertIn("geo\\time", data.columns)
        self.assertTrue(all(str(y) in data.columns for y in range(2014,2020)))
        # values
        self.assertTrue(all(s in {'F','M','T'} for s in data['sex'])) # men, women, total
        self.assertTrue(all(a in {'TOTAL','UNK','0_4','5_9','10_14','15_19','20_24','25_29',
                                  '30_34','35_39','40_44','45_49','50_54','55_59','60_64',
                                  '65_69','70_74','75_79','80_84','85_89','85','90'} for a in data['age']))
        self.assertTrue(all(re.match(r"[A-Z]{2}[0-9]{0,3}", g) for g in data['geo\\time']))
        for y in range(2014,2020):
            self.assertTrue(all(not i or isinstance(i,float) for i in data[f'{y}']))
            

__all__ = ["TestPopulations"]