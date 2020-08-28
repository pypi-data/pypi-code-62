#!/usr/bin/env python3
"""Handling of mqtt messages on flecsimo cell level.

Created on 18.02.2020

@author: Ralf Banning
"""

license_text ="""
    Copyright and License Notice:

    flecsimo area control
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
import argparse
import logging

from flecsimo.base import config
from flecsimo.base.connect import Connector
from flecsimo.base.const import Facility
from flecsimo.roles.callback import RfqMixin, AsgmtMixin, OpdtaMixin, AgentstateMixin


from memory_profiler import profile
from time import sleep


class CellAgentContext(RfqMixin, AsgmtMixin, OpdtaMixin, AgentstateMixin, Connector):
    """Class for cell-agent specific mqtt functionality.
       
    This class initializes the "topology" of a production cell (site, area,
    cell) and set up the subscription to the mqtt server (a.k.a. 'broker').
       
    The main purpose of this class is to assign the callback functions
    to the mqtt client. The callback function are provided by mixin classes
    from the base.callback module:
        
       RfqMixin:    on_rfq callback
       AsgmtMixin:  on_asgmt callback
       OpdtaMixin:  on_opdta callback
       AgentstateMixin: on_agentstart and on_agentstop callbacks
       
    Moreover the class provide to member functions that support enrolment process
    and the quit of operation handling. 
    """
    
    def __init__(self, mode, conf=None, cid=None, broker='localhost'):
        """Initialization of a cell agent.
        
        Args:
            config: JSON string with topology configuration.
            cid:    Cell identifier of mqtt connection.
            broker: Netowrk address of mqtt server (broker)
        """
      
        # Set agent topology
        broker = conf['broker']
        self.typ = Facility.AREATYP
        self.site = conf['site']
        self.area = conf['area']
        self.cell = conf['cell']
        self.database = config.get_db_path(conf['database'])
        self.mode = mode
        self.sender = self.compose_sub(self.site, self.area, self.cell)
        self.myself = self.cell
                       
        super().__init__(self.cell, broker)
                
        # Set subscriptions
        rfq_sub = self.compose_sub(self.site, self.area, 'rfq')
        asgmt_sub = self.compose_sub(self.site, self.area, 'asgmt')  
        opdta_sub = self.compose_sub(self.site, self.area, 'opdta', self.cell)
        
        self.subscription = [(rfq_sub, 0), 
                             (asgmt_sub, 0), 
                             (opdta_sub, 0)
                             ]
        
        # Set connection callbacks from mixins
        self.on_connect = self.on_agentstart
        
        # Add callbacks from mixins
        self.add_callback(rfq_sub, self.on_rfq)
        self.add_callback(asgmt_sub, self.on_asgmt)
        self.add_callback(opdta_sub, self.on_opdta)

    def enrol(self):
        """Let a cell join the area controller facilities.

        Args: 
            topic (str): Topic string.
            payload (str): Message payload in json format.        

        TODO: decide if cfmenrol is used or on publish should be
              enough to be evaluated (fire and forget or two-phase..)

        Scope: Cells only
        """
        
        # TODO: Scope problem: we would need msg here, but it already loaded in mixin...
        #=======================================================================
        # join = msg.Join(self.sender, self.typ, desc=None, loc=None, oplist=None)
        # 
        # publish.single(join.topic, join.payload, hostname=self._broker,
        #                client_id=self._cid, keepalive=10)
        #=======================================================================
        pass

    def quit(self):
        """Announce quit of cell operation to area control.

        TODO: decide if cfmquit is used or on publish should be
              enough to be evaluated (fire and forget or two-phase..)

        Scope: Cells only
        """

        # TODO: Scope problem: we would need msg here, but it already loaded in mixin...        
        #=======================================================================
        # quit = msg.Quit(self.sender)
        # 
        # publish.single(topic, payload, hostname=self.MQTT_IP,
        #                client_id=self._cid)
        #=======================================================================
        pass

@profile
def main():
    """Main process for cell agent.
    
    This code controls the communication between cell-machines and area
    controller and starts operations within the call back functions.
    It provides a normal mode (endless loop) which can be stopped by 
    keyboard input 'Q' and a single run mode for (de)enrol from/at 
    area.
    
    In normal mode the following steps will be executed:
    1. Preparation
        a. Configure cell parameters and subscriptions
        b. Create an agent object from m2m.Cell
        c. Define callback handlers
    2. Start (run the loop in a new thread, where all the call backs will 
        be handled)
    3. Wait for keyboard input 'Q' to handle stop_connection request       
    """
    
    
    # Parse runtime options
    parser = argparse.ArgumentParser(description='Runs an agent controller for manufacturing cells.')  
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--enrol', action='store_true', help='Enrol cell to area controller')
    group.add_argument('-q', '--quit', action='store_true', help='Quit cell operation for area controller.') 
    parser.add_argument('-c', '--config', help='Load configuration from file')
    parser.add_argument('--loglevel', help='Set log level as DEBUG, INFO, WANRING, ERROR or CRITICAL')
    parser.add_argument('-m', '--mode', choices=['AUTO', 'USER'], default='AUTO', help='Set mode as AUTO or USER')
    parser.add_argument('--license', action='store_true', help='Show license and warranty disclaimer.')   
    args = parser.parse_args()
    
    if args.license:
        print(license_text)
        
    if args.loglevel: 
        logging.basicConfig(level=args.loglevel)
  
    if args.config:  
        config_file = args.config
    else:
        config_file = '../conf/config_cell.json'

    conf = config.get_config(config_file, 'Cell')
    
    mode = args.mode
    
    # 1.a Configure cell parameters and subscriptions
 
    # 1.b Create an agent object from m2m.Cell
    agent = CellAgentContext(mode, conf)
    # agent.will(agentstate.topic, agentstate.payload)

    # TODO: re-think on passing celltype, location,...    
    if args.enrol: 
        agent.enrol()
        sleep(1)  # TODO: this has to be understood better...
        exit()
         
    if args.quit:
        agent.quit()
        sleep(1)  # TODO: this has to be understood better...
        exit() 

    # 2. Start thread for loop   
    agent.start_connection()
    
    # 3. Enable graceful shutdown  
    print("***\n*** flecsimo-agent for cell '{}' started in {}-mode".format(agent.sender, mode))
    print("*** Using database {}\n***".format(agent.database))
    input("Press any key to stop execution")
    
    print("Stopping connection...")
    agent.stop_connection(agent.on_agentstop())

       
if __name__ == "__main__":
    
    main()