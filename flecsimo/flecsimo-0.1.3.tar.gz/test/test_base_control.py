"""
Created on 02.03.2020

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
from flecsimo.base import connect


class TestControllerClassInitialization(unittest.TestCase):
    
    def test_class_init(self):

        controller_instance = connect.Connector()
        self.assertEqual(controller_instance._cid, None, 'should be None')
        self.assertEqual(controller_instance._broker, 'localhost', 'should be localhost')
        
        controller_instance = connect.Connector(cid='test_cid', broker='test_broker')
        self.assertEqual(controller_instance._cid, 'test_cid', 'should be test_cid')
        self.assertEqual(controller_instance._broker, 'test_broker', 'should be test_broker')

    def test_class_init_super(self):
        # TODO: write test case test_class_init_super()
        pass
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()