"""Unit tests for base/msg module
 
Created on 02.03.2020

@author: Ralf Banning
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
import json
import datetime
from flecsimo.base import msg
from flecsimo.base.msg import compose_topic
from flecsimo.base.states import AgentStates


class TestDataFormats(unittest.TestCase):
    """ Test if all required message types are present."""
    
    def test_datastructures_defined(self):       
        
        data_required = {'Message',
                         'Enrol',
                         'CfmEnrol',
                         'Quit',
                         'CfmQuit',
                         'Rfq',
                         'Quote',
                         'Asgmt',
                         'Opdta',
                         'Opcfm',
                         'Opstat',
                         'Reading',
                         'Status',
                         }
        
        data_defined = set(dir(msg))
        
        self.assertTrue(data_required < data_defined,
                        "at least one message type is missing")


class TestMessageMethods(unittest.TestCase):
    """Test for member functions of Message and som subtypes."""
    
    def setUp(self):
        self.sender = 'test_sender'
        self.receiver = 'test_receiver'
        self.message_instance = msg.Message(self.sender)
        self.rfq_instance = msg.Rfq(self.sender, 'FUAS', 1000062, 2)
        self.unicast_message = msg.Message(self.sender, self.receiver)
        self.opdta_instance = msg.Opdta(self.sender, self.receiver)
        self.testmsg = msg.Message('test_sender')
        self.testmsg.state = AgentStates.STARTED
    
    def tearDown(self):
        del self.message_instance
        del self.unicast_message
        del self.rfq_instance
        del self.opdta_instance
        del self.testmsg
    
    def test_payload_topic(self):
        
        # Test if topic will be properly set (for base class and one subclass):
        self.assertEqual(self.message_instance.topic, 'test_sender/message')
        self.assertEqual(self.rfq_instance.topic, 'test_sender/rfq')
        self.assertEqual(self.unicast_message.topic, 'test_sender/message/test_receiver')
        self.assertEqual(self.opdta_instance.topic, 'test_sender/opdta/test_receiver')
        
    def test_payload_has_datetime(self):
        
        # Test if 'at' is set:
        payload = dict(json.loads(self.rfq_instance.payload))
        self.assertTrue(payload['at'], 'at-key is missing')
        
        # Test if 'at' contains ISO formatted dat etime string:
        at = payload['at']
        self.assertTrue(datetime.datetime.fromisoformat(at))
    
    def test_format_state(self):       
        
        self.assertTrue(hasattr(self.testmsg, 'state'))

        # Test state splitting with topic getter
        testdict = dict(json.loads(self.testmsg.payload))
        self.assertTrue('state' in testdict, 'Key \'state\' not found.')
        self.assertTrue('state' in testdict, 'Key \'statx\' not found.')
        self.assertEqual(testdict['state'], 4)
        self.assertEqual(testdict['statx'], 'STARTED')

        # Test state splitting with dict getter
        self.assertTrue('state' in self.testmsg.dict, 'Key \'state\' not found.')
        self.assertTrue('state' in self.testmsg.dict, 'Key \'statx\' not found.')
        self.assertEqual(self.testmsg.dict['state'], 4)
        self.assertEqual(self.testmsg.dict['statx'], 'STARTED') 
        
        
class TestModuleFunctions(unittest.TestCase):
    
    def test_compose_topic(self):
        self.assertEqual(compose_topic(), None)
        self.assertEqual(compose_topic('a-part', 'b-part', 'c-part'), 'a-part/b-part/c-part')
        self.assertEqual(compose_topic('a-part', '+', 'c-part'), 'a-part/+/c-part')
        self.assertEqual(compose_topic('a-part', 'b-part', '#'), 'a-part/b-part/#')
        
        # The '#' may not occur inside a topic, only at its end.
        with self.assertRaises(ValueError):
            compose_topic('a-part', '#', 'c-part')
        # TODO: test if args contains list
        # TODO: test if args contains non-str
    
    def test_decompose_topic(self):
        pass
    
    def test_as_dict(self):
        pass
    
    def test_as_dump(self):
        pass
        
        
class TestMessageClassInitialization(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_class_init(self):
        with self.assertRaises(ValueError):
            msg.Message()
            
    def test_class_init_super(self):
        with self.assertRaises(TypeError):
            msg.Rfq()
            
    def test_class_init_without_sender_Rfq(self):
        with self.assertRaises(TypeError):
            _ = msg.Rfq(service='test_service', sfcu='test_sfcu', part='test_part')           
            
    def test_class_init_Rfq(self):
        rfq = msg.Rfq('test_sender', operation='test_operation', sfcu=2, order=1000062, prio=99, site='FUAS')
        self.assertEqual(rfq.topic, 'test_sender/rfq')
        self.assertEqual(rfq.operation, 'test_operation')
        self.assertEqual(rfq.sfcu, 2)
        self.assertEqual(rfq.order, 1000062)
        self.assertEqual(rfq.prio, 99) 
        self.assertEqual(rfq.site, 'FUAS')
        
    def test_class_init_Status(self):
        status = msg.Status('test_sender', typ="C", state=AgentStates.STARTED)
        self.assertEqual(status.topic, 'test_sender/status')
        self.assertEqual(status.typ, 'C')
        self.assertEqual(status.state.name, "STARTED")
        self.assertEqual(status.state.value, 4)


if __name__ == "__main__":

    unittest.main()
