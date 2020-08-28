"""Unit tests for roles/order_processing module.

TODO: ... allmost evereything...

Note: currently main problem, that all SQL-statements are prepared as local string,
    which makes them inaccessible for unit-testing. So: only "black-box"testing is
    possible.

Created on 10.07.2020

@author: Ralf
"""

"""
    Copyright and License Notice:

    flecsimo sfc processing
    Copyright (C) 2020  Ralf Banning, Bernhard Lehner and Frankfurt University 
    of Applied Sciences.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import unittest
import sqlite3


class Test(unittest.TestCase):


    def setUp(self):
        self.db = "../db/site.db"
        
        # Load script to create memory data base
        with open("test_order_processing/testdata_site_db.sql", "r") as scriptfile:
            script = scriptfile.read()
            
        self.tconn = sqlite3.connect(":memory:")
        self.tconn.row_factory = sqlite3.Row 
        self.tcur = self.tconn.cursor()

        # Set up test database 
        with self.tconn:
            self.tcur.executescript(script)



    def tearDown(self):
        self.tconn.close


    def testSetup(self):
        select_order="""SELECT * FROM 'order'"""
        
        with self.tconn:
            self.tcur.execute(select_order)
            rows = self.tcur.fetchall()
            
        print("Content of order table:", [dict(r).items() for r in rows])
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()