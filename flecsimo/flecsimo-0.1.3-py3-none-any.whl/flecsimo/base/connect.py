#!/usr/bin/env python
"""Enable machine-to-machine communication.

This module provide wrapping classes for mqtt connection handling as used
for flecsimo set up. 

Created on 30.01.2020

@author: Ralf Banning
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
import logging
import paho.mqtt.client as mqtt

# TODO: find generla concention for module log handler
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class Connector(object):
    """Provide connection methods to mqqt-client as useful within flecsimo.
    
    This class provides wrapping methods of mqtt-client class to expose
    only those functionalities which are really needed in flecsimo 
    m2m communication. Some wrappers (as "subscribe" provide additional
    check and evaluation functionality.
    
    TODO: provide standard overrides for call backs
    """

    def __init__(self, cid=None, broker='localhost'):
        """Initialize system variables and prepare MQTT connection..

        Args:
            ctlid (str): Unique identifier for the client or ''.
            broker (str): Identifier to connect the _broker, i.e. IP-address.

        Scope: General, for all controller
        """
        # Default
        self.subscription = None
   
        # Assign arguments     
        self._cid = cid
        self._broker = broker
        self._client = mqtt.Client(cid)
        self._client.on_message = self._on_message
        self._client.on_log = self._on_log 

    @property
    def on_connect(self):
        return self._client.on_connect

    @on_connect.setter
    def on_connect(self, on_connect):
        self._client.on_connect = on_connect
    
    @property
    def on_message(self):
        return self._client.on_message

    @on_message.setter
    def on_message(self, on_message):
        self._client.on_message = on_message

    @property
    def on_log(self):
        return self._client.on_log

    @on_log.setter
    def on_log(self, on_log):
        self._client.on_log = on_log
              
    def _on_message(self, client, userdata, message):
        """Internal default message handler.
        
        TODO: decide if useful!
        """
        _log.debug("Received message id %s with payload %s", message.mid, str(message.payload.decode("utf-8")))
        
    def _on_log(self, client, userdata, level, buf):
        """Internal default logger."""
        _log.debug("log: %s", buf) 
        
    def compose_sub(self, *args):
        """Compose a mqtt compatible subscription string. 
    
        This methods builds a topic string suitable for mqtt application messages.
        Topics may contain '+' and '#' wildcards. Whereas '+' could be used at any
        position, '#' is only allowed as last element.
    
        Args:
            *args: Tuple of subscription path elements. 
        
        Returns:
            The composed subscription if args were provided, else None.
            
        TODO: find a solution to prevent malformed topics, esp. those
            using a message tpye names in sender or receiver part ("blacklisted").
            Clearly this functionality should be designed "lean", since it will be used 
            quite often.
        """
            # TODO: handle exection if args contains list
        if args:
            if '#' in args:
                if args.index('#') < len(args) - 1:
                    raise ValueError("Wildcard '#' is allowed only at the end of a subscription!")
                
            sub = '/'.join(args)
            return sub
        
    def add_callback(self, sub, callback):
        """Wrapper for mqtt client.message_callback_add().

        Args:
            sub (str): Subscription topic.
            callback (func): Reference to callback function.

        Scope: General, for all controller
        """
        self._client.message_callback_add(sub, callback)        

    def publish(self, topic, payload):
        """Wrapper for mqtt publish

        Args: 
            topic (str): Topic string.
            payload (str): Message payload in json format.

        TODO:
            Add control if publish is done
            give control on QOS

        Scope: General, for all controller
        """
        rc = self._client.publish(topic, payload, qos=0)
        
        _log.debug("publish returns %s", rc) 

    def subscribe(self, topic):
        """Wrapper for mqtt subscribe

        Args:
            topic (str): Topic string.

        TODO:
            Add control if subscription is achnowledged.     
            (see: http://www.steves-internet-guide.com/checking-mqtt-subscriptions-code/)
            Provide function to handle a list of subscriptions.

        Scope: General, for all controller
        """
        rc = self._client.subscribe(
            topic, qos=0, options=None, properties=None)
        
        # TODO: to be changed
        _log.debug("subscription returns %s", rc) 

    def will(self, topic, payload):
        """Set (last) will of cell.

        Wraps client.will_set.

        Args:
            topic (str): Topic string.
            payload (str): Message payload in json format.

        Scope: General, for all controller            
        """
        self._client.will_set(topic, payload, 0, retain=True)
        
    def start_connection(self):
        """Start cell operation and listen to subscribed messages.
        
        Connects to a broker and subcribes to a topic or list of topics
        (if provided) and will start client loop in any case.
        
        Args:
            topic: topic or list of topics to be subscribed to.
        
        TODO: figure out, if (and how) async connection should be used.
            (it does not work just to exchange connect with connect_async
            
        TODO: handle return code from connect.
    
        Scope: General, for all controller
        """     
        self._client.connect(self._broker)
        
        if self.subscription:
            self.subscribe(self.subscription)
        
        self._client.loop_start()

    def stop_connection(self, on_stopfunc):
        """Stop cell operations and shut down connections gracefully.

        Scope: General, for all controller that used start_connection
        """
        _log.debug("Call on_stopfunc...")
        on_stopfunc
        
        _log.debug("Call disconnect...")
        self._client.disconnect()

        _log.debug("Stop loop.")
        self._client.loop_stop()
