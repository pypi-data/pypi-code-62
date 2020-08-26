#!/usr/bin/env python
# -*- coding: utf-8 -*-

# py_tools_ds
#
# Copyright (C) 2019  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
test_coord_trafo
----------------

Tests for `py_tools_ds.geo.coord_trafo` module.
"""

import unittest
from shapely.geometry import Polygon

from py_tools_ds.geo.coord_trafo import reproject_shapelyGeometry


poly_local = Polygon([(5708.2, -3006), (5708, -3262), (5452, -3262), (5452, -3006), (5708, -3006)])


class Test_reproject_shapelyGeometry(unittest.TestCase):

    def test_reproject_shapelyGeometry(self):
        poly_lonlat = reproject_shapelyGeometry(poly_local, 32636, 4326)
        self.assertTrue(isinstance(poly_lonlat, Polygon))
