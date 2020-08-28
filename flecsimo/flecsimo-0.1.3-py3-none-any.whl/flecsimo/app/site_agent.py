#!/usr/bin/env python3
"""Handling of mqtt messages on flecsimo site level.

Created on 30.05.2020

@author: Ralf Banning
"""

license_text = """ 
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
import argparse
import logging
# from time import sleep

from flecsimo.base import config
from flecsimo.base.connect import Connector
from flecsimo.base.const import Facility
from flecsimo.roles.callback import EnrolMixin, QuoteMixin, OpdtaMixin, ReportMixin, AgentstateMixin


class SiteAgentContext(EnrolMixin, QuoteMixin, OpdtaMixin, ReportMixin, AgentstateMixin, Connector):
    """Class for site control specific mqtt functionality.
    
    This class initializes the "topology" of a an site agent and set up the 
    subscription to the mqtt server (a.k.a. 'broker').
       
    The main purpose of this class is to build the context of the area_agent, 
    i.e. to assign the callback functions to the mqtt client. 
    
    The callback function are provided by mixin classes from the 
    roles.callback module:
        
        RfqMixin:    on_rfq callback
        AsgmtMixin:  on_asgmt callback
        OpdtaMixin:  on_opdta and on_opcfm callback
        EnrolMixin:  on_enrol and on_quit callback
        QuoteMixin:  on_quote callback
        ReportMixin: on_opstat and on_reading callback
        AgentstateMixin: on_agentstart and on_agentstop callback    
    """

    def __init__(self, mode, conf=None, cid=None, broker='localhost'):
        """Initialization of an site agent.
        
        Args:
            config: JSON string with topology configuration.
            cid:    Cell identifier of mqtt connection.
            broker: Netowrk address of mqtt server (broker)
        """
        # Set agent topology.
        self.mode = mode
        broker = conf['broker']
        self.typ = Facility.SITETYP
        self.site = conf['site']
        self.database = config.get_db_path(conf['database'])
        self.sender = self.site
        
        super().__init__(cid, broker)

        # Set subscriptions
        enrol_sub = self.compose_sub(self.site, '+', 'enrol')
        quit_sub = self.compose_sub(self.site, '+', 'quit')
        quote_sub = self.compose_sub(self.site, '+', 'quote')
        opcfm_sub = self.compose_sub(self.site, '+', 'opcfm')
        opstat_sub = self.compose_sub(self.site, '+', 'opstat')


        self.subscription = [(enrol_sub, 0),
                             (quit_sub, 0),
                             (quote_sub, 0),
                             (opcfm_sub, 0),
                             (opstat_sub, 0)
                            ]        
        
        # Set connection callbacks from mixins
        self.on_connect = self.on_agentstart
        self.on_disconnect = self.on_agentstop  
        
        # Add topic call backs from mixins      
        self.add_callback(enrol_sub, self.on_enrol)
        self.add_callback(quit_sub, self.on_quit)
        self.add_callback(quote_sub, self.on_quote)
        self.add_callback(opcfm_sub, self.on_opcfm)
        self.add_callback(opstat_sub, self.on_opstat)


def main():
    """Main process for cell agent.
    
    This code controls the communication between cell-machines and area
    controller and starts operations within the call back functions.
    It provides a normal mode (endless loop) which can be stopped by 
    keyboard input 'Q' and a single run mode for (de)registration from/at 
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
    parser = argparse.ArgumentParser(description='Runs an agent controller for site.')    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--enrol', action='store_true', help='Enrol site')
    group.add_argument('-q', '--quit', action='store_true', help='Quit site.')
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
        config_file = '../conf/config_site.json'

    conf = config.get_config(config_file, 'Site')
    
    mode = args.mode
     
    # 1.a Configure cell parameters and subscriptions
 
    # 1.b Create an agent object from m2m.Cell
    agent = SiteAgentContext(mode, conf)
    # TODO: reactivate agent will
    # agent.will(agentstate.topic, agentstate.payload)

    # 2. Start thread for loop   
    agent.start_connection()
    
    # 3. Enable graceful shutdown
    # TODO: redesign
    print("***\n*** flecsimo-agent for site '{}' started in {}-mode\n***\n".format(agent.sender, mode))
    input("Press any key to stop execution")
    
    print("Stopping connection...")
    agent.stop_connection(None)


if __name__ == '__main__':
    
    main()
