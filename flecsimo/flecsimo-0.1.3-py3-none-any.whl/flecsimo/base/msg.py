"""Message structures for machine communication (m2m) in flecsimo.

This module provides roles container for machine-to-machine communication using 
the MQTT protocol. Messages in this protocol (so called "application messages")
consist at least of a topic and a payload. MQTT communication in flecsimo 
is designed in a way, that the topic will express the sender identification
(written as a topology 'path', e.g. site_name/area_name/cell_name) plus the
message type. Messages are sent via a publish protocol and received by 
subscribing a list of topics. 

Typical usage example:
    (Assumes, a MQTT client c has been instantiated before)
    
    reg = Enrol(cell_name, celltype='mfc', services=['D05','D10'])
    reg.loc = 'X01:Y01-IX02:IY01-OX02:OY01'
    client.publisch(reg.topic, reg.payload) 

Notes:
    This modules is designed for MQTT version 3, using paho-mqtt client lib
    and eclipse mosquitto as MQTT server. The MQTT interfaces are not part of 
    this module.
    
    If run with Python version lower as 3.7, collection type has to be used
    
    The classes could also be defined as @dataclasses, but this feature is 
    available only from Python version 3.7 onwards - so this could be a 
    task for later redesign.
    
Requires:
    Python version: 3.7 (garantee of dictionary order)

Created on:
     18.02.2020

@author: 
    Ralf Banning   
"""

""" 
    Copyright and License Notice:

    flecsimo site control
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
import datetime
import json


def compose_topic(*args):
    """Compose a mqtt compatible topic string. 
    
    This methods builds a topic string suitable for mqtt application messages.
    Topics may contain '+' and '#' wildcards. Whereas '+' could be used at any
    position, '#' is only allowed as last element.
    
    Args:
        *args: Tuple of topic elements. 
        
    Returns:
        The composed topic if args were provided, else None.
        
    TODO: This function is "moved" to connect, since this module is handling
        subscription (which may contain wildcards). This is not the case with
        topics - therefore it has to be discussed, whether we need a compose_topic
        in this module and if the decompose_topic is really used and where.
    """
    # TODO: handle exeuction if args contains list
    if args:
        if '#' in args:
            if args.index('#') < len(args) - 1:
                raise ValueError("Wildcard '#' is allowed only at the end of a topic!")
            
        topic = '/'.join(args)
        return topic


def decompose_topic(topic):
    """Split flecsimo topic into sender and message type.
      
    Args: 
        topic (str): A topic string
        
    Returns:
        (sender, sep, message_type): A 3-tupel containing the part before
            the last occurrence of the separator (sender), the separator 
            itself and the part after the last separator (message_type).
              
    TODO: it seems that this function is not really used elsewhere - think
        of delete it. 23-06-2020
        
        Well, could be useful to extract sender from topic in callbacks as
        'get_sender()' 24-06-2020
    """
    return topic.rpartition('/')


def as_dict(message_topic, message_payload):
    """Decode mqtt message payload as dict and add topic."""
    if type(message_payload) is str:
        data = dict(json.loads(message_payload))
    else:
        data = dict(json.loads(str(message_payload.decode("utf-8"))))

    data.update({"topic": message_topic})
    return data


def as_dump(payload):
    """Return a formatted string from a dictionary.
    
    Args:
        payload (dict): payload to dump
    """    
    return(json.dumps(payload, indent=4))


class Message(object):
    """Base class for messaging roles.

    Create a message object comprising a topic string and a time-stamp.
    The topic string is composed of the sender identification 
    (sitename/area_id/cell_id) and the message name, which equals the class 
    name. The payload is composed of all class attributes beside of '_topic'.

    Example:
        If Opstat is a subclass of Message, an Opstat('FUAS/a-01/mfc-3') instance 
        has properties Opstat.topic and Opstat.payload, which will return value 
        'FUAS/a-01/mfc-3/Opstat' and the spectific payload. 

    Attributes:
        sender (str): name of the sender identification 
        at (datetime): timestamp
    """

    def __init__(self, sender=None, receiver=None):
        """Initialize class members."""
        if sender:  
            _topiclist = [sender, type(self).__name__.lower()] 
            if receiver:     
                _topiclist.append(receiver)
            self._topic = "/".join(_topiclist)
        else:
            raise ValueError("Sender is 'None'.")
        
    def _format_state(self, dictionary):
        """Expand state attribute for Enum-type state objects
        
        If a dictionary has a 'state' attribute, this function analyzes
        if it's value provide a name and value function (which is typically the 
        case if the 'state' is of Enum type. In this case, it splits the state 
        object into state value and state name (textual description) and maps 
        these components to the 'state' and 'statx' dictionary element 
        respectively.
        
        Args:
            dictionary (dict): the dictionary to be formated.
        """
        if 'state' in dictionary:
            try:
                state = self.state.value
                descr = self.state.name
            except TypeError:
                raise
            except:
                state = self.state
                descr = None
                
            dictionary.update({'state': state, 'statx': descr})
            
        return dictionary
        
    @property
    def topic(self):
        return self._topic

    @property
    def payload(self):
        """Transform class members without 'topic' into a message string.
        
        The function creates a copy of the class dictionary and 'strips off' 
        the topic attribute. If a state attribute is present, it patches a
        'state' and 'descr' field to the message. If the state is given as
        an enumearation member it maps the value to the state-field and the 
        name to the description-field. If this is not the case it tries to 
        map the state to the state-field.
        
        In any case, an 'at-field' is appended to the message containing 
        the current roles and utc-time in iso-Format.
        
        Raises:
            TypeError, if state is an enumeration class instead of a member. 
            
        Return:
            The json formatted message as a string.
        """                       
        payload = self.__dict__.copy()
        del payload['_topic']   
        
        payload = self._format_state(payload)
                       
        at = datetime.datetime.utcnow()
        payload.update({'at': at.isoformat()})
        
        return json.dumps(payload)
    
    @property
    def dict(self):
        """Return message ak dictionary.
        
        The function is similar to the payload property but 
        - includes the topic
        - returns a dictionary instaed of string and 
        """
        dictionary = self.__dict__.copy()
        
        dictionary = self._format_state(dictionary)
                
        dt = datetime.datetime.utcnow()
        dictionary.update({'at': dt.isoformat()})
        
        return dictionary


class Enrol(Message):
    """Enrol cell with an area controller.
    
    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        type (str): identify cell type as of 'mfc', 'wh', ... 
        loc (str): location identifier of cell and cell in/out.
        services  (list): list of provided services.
    """

    def __init__(self, sender, typ=None, desc=None, loc=None, oplist=None):
        super().__init__(sender)
        self.name = sender
        self.typ = typ
        self.desc = desc
        self.loc = loc
        self.oplist = oplist


class CfmEnrol(Message):
    """Acknowledgement for cell registration by area controller.
    
    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        cell (str): cell name / identification. 
        mid (int): message id of request.
    """

    def __init__(self, sender, cell=None, mid=None):
        super().__init__(sender)
        self.cell = cell
        self.mid = mid


class Quit(Message):
    """De-register a cell from an area controller.
    
    This message has to be used, if a cell should be moved to another location 
    inside an area or to another area.
    
    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.   
        
    Attributes:
        cell (str): cell name / identification. 
    """    

    def __init__(self, sender, facility):
        super().__init__(sender)
        self.sender = sender
        self.facility = facility


class CfmQuit(Message):
    """Acknowledgement of cell de-registration by area controller
    
    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.   
        
    Attributes:
        cell (str): cell name / identification. 
        mid (int): message id of request.
    """   

    def __init__(self, sender, cell=None, mid=None):
        super().__init__(sender)
        self.cell = cell
        self.mid = mid

# TODO: Rfq, Quote and Asgmt have nearly same structure - derive from intermediate type?

class Rfq(Message):
    """Request an operation.

    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        operation (str): operation code for requested operation.
        sfcu (str): shop floor-control-unit identification. 
        part (str): part number.
        
    Example:
        Topic: FUAS/area_1/rfq
        Payload: 
        {
            "site": "FUAS", 
            "order": 1000063", 
            "sfcu": 21, 
            "pds": 1,
            "operation": "27-DRILLING", 
            "supplier": "cell-2"
            "typ": "C"
            "due": "2020-10-31", "prio": 0, "statx": "initial", "at": "2020-07-03 15:10"}
}
    """

    def __init__(self, sender, site, order, sfcu, pds=None, operation=None, supplier=None, typ=None, due=None, prio=0, state=None):
        super().__init__(sender)
        
        self.site = site
        self.order = order
        self.sfcu = sfcu  
        self.pds = pds
        self.operation = operation
        self.supplier = supplier
        self.typ = typ
        self.due = due 
        self.prio = prio
        self.state = state


class Quote(Message):
    """Offering an operation.

    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        tenderer (str): cell name / identification. 
        sfcu (str): shop floor-control-unit identification.
    """  

    def __init__(self, sender, site, order, sfcu, pds=None, operation=None, supplier=None, typ=None, due=None, prio=0, state=None):
        super().__init__(sender)
        
        self.site = site
        self.order = order
        self.sfcu = sfcu  
        self.pds = pds
        self.operation = operation
        self.supplier = supplier
        self.typ = typ
        self.due = due 
        self.prio = prio
        self.state = state

        
class Asgmt(Message):
    """Assign an operation to an area or cell.

    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        sfcu (str): shop floor-control-unit identification.
        sender (str): sender of assignment (in the role of a client).
        supplier (str): receiver of assignment. 
        prio (int): priority indicator.
        dhash (str): hash of the associated opdta message payload.
    """

    def __init__(self, sender, site, order, sfcu, pds=None, operation=None, supplier=None, typ=None, due=None, prio=0, dhash=None, state=None):
        super().__init__(sender)
        
        self.site = site
        self.order = order
        self.sfcu = sfcu  
        self.pds = pds
        self.operation = operation
        self.supplier = supplier
        self.typ = typ
        self.due = due 
        self.prio = prio
        self.state = state
        self.dhash = dhash

        
class Opdta(Message):
    """Send operation data (sfcus and tasks)

    Args:
        sender (str): the sender identification as shown in topic.
        data (dict): operation data.
    
    Attributes:
        data (dict): operation data. 
    """    

    def __init__(self, sender, receiver, data={}):
        super().__init__(sender, receiver)
        self.data = data        


class Opcfm(Message):
    """Send confirmation of received Opdta.

    """   

    def __init__(self, sender):
        super().__init__(sender)
        
        
class Opstat(Message):
    """Report operational status.

    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        sfcu (str): shop floor-control-unit identification. 
        part (str): part number.
        state (int): status of operation.
        descr (str): textual representation of state.
    """   

    def __init__(self, sender, site, order, sfcu, operation, state):
        super().__init__(sender)
        self.site = site
        self.order = order
        self.sfcu = sfcu
        self.operation = operation
        self.state = state


class Reading(Message):
    """Report readings from device.

    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        observ (str): shop floor-control-unit identification. 
        value (str): part number.
        unit (int): status of operation.
    """    

    def __init__(self, sender, source=None, value=None, unit=None):
        super().__init__(sender)
        self.source = source
        self.value = value
        self.unit = unit


class Status(Message):
    """Acknowledgement for cell registration by area controller.
    
    Args:
        sender (str): the sender identification as shown in topic.
        named args for each attribute.
    
    Attributes:
        typ (str): type of sender ('C', 'STN', 'WH', 'A', 'S', 'TXP' ). 
        state: status of sender as member of a Enum-class or just a string.
    """

    def __init__(self, sender, typ=None, state=None):
        
        super().__init__(sender)
        self.typ = typ
        self.state = state
                
