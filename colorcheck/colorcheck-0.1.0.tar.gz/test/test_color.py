#! /usr/bin/env python

# Test suite for color parameters calculations (luminance and contrast)

import cssutils
import unittest

from colorcheck.color import *

LIGHTBLUE = cssutils.css.ColorValue("lightblue")
RED = cssutils.css.ColorValue("red")
GREENYELLOW = cssutils.css.ColorValue("greenyellow")
ORANGE = cssutils.css.ColorValue("orange")

class TestColor(unittest.TestCase):
    def test_luminance(self):
        self.assertAlmostEqual(luminance(LIGHTBLUE), 0.6370914)
        self.assertAlmostEqual(luminance(RED), 0.2126)
        self.assertAlmostEqual(luminance(GREENYELLOW), 0.8060947)
        self.assertAlmostEqual(luminance(ORANGE), 0.4817027)

    def test_contrast(self):
        self.assertAlmostEqual(contrast(LIGHTBLUE, RED), 2.6164943)
        self.assertAlmostEqual(contrast(LIGHTBLUE, GREENYELLOW), 1.2459692)
        self.assertAlmostEqual(contrast(LIGHTBLUE, ORANGE), 1.2922474)
        self.assertAlmostEqual(contrast(RED, GREENYELLOW), 3.2600713)
        self.assertAlmostEqual(contrast(RED, ORANGE), 2.0247626)
        self.assertAlmostEqual(contrast(GREENYELLOW, ORANGE), 1.6101005)

if __name__ == "__main__":
    unittest.main()
