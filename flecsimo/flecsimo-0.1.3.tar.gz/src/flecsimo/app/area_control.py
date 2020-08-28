#!/usr/bin/env python3
"""Command interpreter for controlling area processes

This module provides a wrapper for the area_context which implements the 
interactions of the shop floor control processing use cases.

Architectural note: 
    This component may be seen as a replacement for a "GUI", and acts mainly 
    for the controller-part. The "order_context" object follows the ideas of 
    Reenskaug and Coplien, to factor out use case algorithms and business logic 
    from pure domain data object (the database in this case) in to abstract 
    role models which are mixed into the data objects at runtime. 

Created on 30.05.2020

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
import cmd
import logging

from pyreadline import Readline

from flecsimo.base import config
from flecsimo.base.connect import Connector
from flecsimo.roles.controller import SchedulerMixin, ProcureMixin, TenderMixin


readline = Readline()

class AreaControlContext(SchedulerMixin, ProcureMixin, TenderMixin, Connector):
    """ Provide methodful roles for site control."""
    
    def __init__(self, database, cid, broker):
        
        super().__init__(cid=cid, broker=broker)
        self.database = database


class AreaCmd(cmd.Cmd):
    """Command wrapper for area control workflow.""" 
    
    intro = """
    *************************************************************************
    * Welcome to the flecsimo area controller.                              *
    *                                                                       *
    * Copyright (C) 2020  Ralf Banning, Bernhard Lehner and Frankfurt       * 
    * University of Applied Sciences.                                       *
    *                                                                       *
    * This program comes with ABSOLUTELY NO WARRANTY                        *
    *                                                                       *
    * Type help or ? to list commands.                                      *
    *                                                                       *
    *************************************************************************
    """

    def __init__(self, conf, database):
        super().__init__(completekey='TAB')
        self.database = database
        self.conf = conf
    
    def _parse(self, arg):
        """Normalizes cmd arguments for called functions.
        
        Converts a kword argument string (as given by cmd interpreter) in to a
        dictionary. Providing an argmument string with non-keyword arguments
        will raise an exception. If the argument strin is empty, an empty dictionary
        is returned.
        
        Note: all argument values should be entered without any quotes. All 
            arguments will be handled internally as str.
            
        Examples:
            create_order(material=FXF-1100, variant=col:red, qty=2) is ok
            create_order(FXF-1100, col:red, qty=2) will fail.
            
        Args:
            arg (str)       
        """       
        if arg:
            arg = arg.replace('\'', '')
            arg = arg.replace('\"', '')     
            arg_as_dict = dict(x.split("=") for x in arg.strip('()').split(', '))
        else:
            arg_as_dict = dict()
            
        return arg_as_dict
        
    def preloop(self):      
       
        # Read config
        self.site = self.conf['site']
        self.area = self.conf['area']

        self.broker = self.conf['broker']
        self.prompt = 'Area:{}>'.format(self.area)

        # Start mqtt connection     
        print("Connecting {} area to mqtt-server at {} ...".format(self.site, self.broker))  
        try:
            self.control = AreaControlContext(self.database, self.area, self.broker)
            self.sender = self.control.compose_sub(self.site, self.area)
            self.control.start_connection()
            
        except ConnectionRefusedError as e:
            print(e, "\nArea controller will be stopped.")
            exit()
    
        
    def do_enrol(self, arg):
        topic=None
        payload=None
        
        self.order_context.enrol(topic, payload)
    
    def do_quote(self, arg):
        """Quote for a received site rfq."""
        pass
    
    def do_request_quote(self, arg):
        """Request a quotation for an sfcu/operation from cells."""
        pass
    
    def do_release_sfcu(self, arg):
        """Assign an sfcu to cell and send opdta"""
        pass
      
    def do_quit(self, arg):
        topic=None
        payload=None
        
        self.order_context.quit(topic, payload)
          
    def do_bye(self, arg):
        """ Quit the application."""
        print('Thank you for using area:{}'.format(self.area))
        self.close()
        return True  
    
    def close(self):
        # Stop the mqtt connection.
        print("Stopping mqtt connection ...")
        
        self.control.stop_connection(None)

def main():
    """Main process for area control.
    
    Parse arguments, read configuration, assign database, instantiate SiteControl 
    and start command loop.
    """
    # Parse runtime options
    parser = argparse.ArgumentParser(description='Wrapper for area order_context. Implements the interactions of the sfc processing use cases.')
    parser.add_argument('-c', '--config', help='Load configuration from file')    
    parser.add_argument('--database', help='Database to use for site control')
    parser.add_argument('--loglevel', help='Set log level as DEBUG, INFO, WANRING, ERROR or CRITICAL')
    parser.add_argument('--license', action='store_true', help='Show license and warranty disclaimer.')
    args = parser.parse_args()
        
    if args.license:
        print(license_text)
    
    if args.loglevel: 
        logging.basicConfig(level=args.loglevel)
        
    if args.config:  
        config_file = args.config
    else:
        config_file = config.get_conf_path('config_area.json')
    
    conf = config.get_config(config_file, 'Area')       
    
    if args.database:  
        database = args.database
    else:
        database = config.get_db_path('area.db')

    # Start command loop
    AreaCmd(conf, database).cmdloop()

if __name__ == '__main__':
    
    main()