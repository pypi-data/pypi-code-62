#!/usr/bin/env python3
"""Command interpreter for controlling site processes

This module provides a wrapper for the site_context which implements the 
interactions of the order processing use cases.

Architectural note: 
    This component may be seen as a replacement for a "GUI", and acts mainly 
    for the controller-part. The "SiteControlContext" object follows the ideas of 
    Reenskaug and Coplien, to factor out use case algorithms and business logic 
    from pure domain data object (the database in this case) in to abstract 
    role models which are mixed into the data objects at runtime. 

Created on 25.05.2020

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
import cmd
import logging

from pyreadline import Readline
# from memory_profiler import profile

from flecsimo.base import config
from flecsimo.base.connect import Connector
from flecsimo.base.const import Facility
from flecsimo.base.states import OrderStates, ScheduleStates
from flecsimo.roles.controller import OrderMixin, SchedulerMixin, ProcureMixin, TenderMixin

readline = Readline()


class SiteControlContext(OrderMixin, SchedulerMixin, ProcureMixin, TenderMixin, Connector):
    """ Provide methodful roles for site control."""
    
    def __init__(self, database, cid, broker):
        
        super().__init__(cid=cid, broker=broker)
        self.database = database


class SiteCmd(cmd.Cmd):
    """Command wrapper for site control workflow.""" 
    
    intro = """
    *************************************************************************
    * Welcome to the flecsimo site controller.                              *
    *                                                                       *
    * Copyright (C) 2020  Ralf Banning, Bernhard Lehner and                 * 
    * Frankfurt University of Applied Sciences.                             *
    *                                                                       *
    * This program comes with ABSOLUTELY NO WARRANTY                        *
    *                                                                       *
    * Type help or ? to list commands.                                      *
    *                                                                       *
    *************************************************************************
    """

    def __init__(self, conf, database):
        """Initialize configuration of SiteCmd."""
        super().__init__(completekey='TAB')
        self.database = database
        self.conf = conf
    
    def _parse(self, arg):
        """Normalizes cmd arguments for called functions.
        
        Converts a kword argument string (as given by cmd interpreter) in to a
        dictionary. Providing an argument string with non-keyword arguments
        will raise an exception. If the argument string is empty, an empty 
        dictionary is returned.
        
        Note: all argument values should be entered without any quotes. All 
            arguments will be handled internally as str.
            
        Examples:
            new_order(material=FXF-1100, variant=col:red, qty=2) is ok
            new_order(FXF-1100, col:red, qty=2) will fail.
            
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
        """Setup mqtt connection and site roles on startup of command loop."""          
        # Read config
        self.site = self.conf['site']
        self.broker = self.conf['broker']
        self.prompt = 'Site:{}>'.format(self.site)
        self.sender = self.site
        self.myself = self.site

        # Start mqtt connection     
        print("Connecting {} site to mqtt-server at {} ...".format(self.site, self.broker))  
        try:
            self.control = SiteControlContext(self.database, self.site, self.broker)
            self.control.start_connection()
            
        except ConnectionRefusedError as e:
            print(e, "\nSite controller will be stopped.")
            exit()
   
    def do_create_order(self, arg):
        """Create a new order.
        
        Create the minimum data for a flecsimo order.
 
        TODO: improve rc-handling.
               
        Args: 
            material (str):    Material number.
            qty (float):       Total quantity of products (default=1.0).
            unit (str):        Base unit of measure (default=PCE).
            variant (str):     Variant code (default=None).
            
        Example:
            material=FXF-1100, qty=1.0, variant=col:red
        """
        # 1. Create new order and print result text.
        rc = self.control.new_order(site=self.site, **self._parse(arg))
        print(rc[3])        

        # 2. Handle non-set parameters.        
        if rc[2]:
            
            # There are not-set parameters.
            # Set order number from return.
            order = rc[1]
            
            answer = input("This order requires to set missing parameters. Do You want to enter these parameters now? ([Y]es or [N]o):").upper()
            
            if answer == 'Y':
                # Get parameter types where value is missing.
                params = self.control.get_order_param(site=self.site, order=order)
                
                # Ask for parameter value.
                for p in params:
                    param_typ = p['param_typ']
                    param_value = input("Enter parameter value for typ {}:".format(param_typ))
                    
                    if param_value:
                        # set value
                        self.control.set_order_param(self.site, order, param_typ, param_value)
                    else:
                        print("Value missing. Skip insert.")
                
            elif answer == 'N':
                print("You have chosen 'No'. Be aware, that You have to provide the parameters before order release.")
            else:
                print("Your answer {} is unknown. Use set_order_param command to set parameters.".format(answer))

    def do_plan_order(self, arg):
        """Plan execution of an order in the flecsimo systems.
        
        Perform the following workflow:
        1. Create the sfcus and update order status.
        2. Create the order operation data (opdta) and update order status.
        3. Ask for order due date.
        4. Create demands in dmsbook per sfcu (demand supply matching).
        5. Create supply position for suppling area.
                     
        TODO: Needs redesign when real planing algorithms are defined.   
        
        Args:
            order (int):    order number.
            supplier (str): dedicated supplier for task (area-code).
        """
        # 0. Initialize
        order = self._parse(arg)['order']
        supplier = self._parse(arg)['supplier']
        pds=self.control.get_pds(self.site, order)
        
        try:
            prio = self._parse(arg)['prio']
        except:
            prio = 0            

        state = ScheduleStates.PLANNED.value
        statx = ScheduleStates.PLANNED.name
              
        # 1. Create the sfcus and update orderv status
        sfculist = self.control.new_sfcu(self.site, order)
        
        print("Created sfcus:", sfculist)
        
        # 2. Create the order operation data (opdta) and update order status.
        self.control.new_opdta(self.site, order)
       
        # 3. Ask for order due date.
        due = input("Enter due date [YYYY-MM-DD] for demand: ")
        
        
        # 5. Create tasklist record for suppling area.
        for sfcu in sfculist:
            schedule = self.control.new_schedule(site=self.site,
                                                order=order,
                                                sfcu=sfcu,
                                                pds=pds,
                                                operation=None,
                                                supplier=supplier,
                                                typ=Facility.AREATYP.value,
                                                due=due,
                                                prio=prio,
                                                state=state,
                                                statx=statx)
        
            print("Created new_schedule {} for sfcu {} and supplier {}.".format(schedule, sfcu, supplier))
            
        self.control.set_order_state(self.site, order, OrderStates.PLANNED)

    def do_release_order(self, arg):
        """ Release an order to production.
        
        Perform the following workflow:
        - Publish mulitcast assignemnt to selected area (update order book)
        - Publish unicast operation data to selected area (update order book).
        - update order status.
                              
        Args:
            order (int):       Order number.
            
        Examples:
            Testdata may be found in test/test_order_processing:
                testdata_asgmt.json
                testdata_opdta.json
        """

        # TODO: needs error handling, if arguments not set.
        argd = self._parse(arg)
        order = argd['order']
        
        asgmtlist = self.control.get_asgmt(self.sender, self.site, order)
                                
        if asgmtlist:                         
            for asgmt in asgmtlist:      
                # Publish assignemnts (asgmt)
                self.control.publish(asgmt.topic, asgmt.payload)
                print("Assignment for sfcu {} published.".format(asgmt.sfcu))    
                                
            # Bulk update schedule status
            self.control.update_schedule(self.site, 
                                         order, 
                                         ScheduleStates.ASSIGNED)
           
            # TODO: this is only true if we assign complete orders to an area:
            supplier = asgmtlist[0].supplier
           
            # Publish manufacturing instructions (opdta)                    
            opdta = self.control.get_opdta(self.site, self.site, order, supplier)
            self.control.publish(opdta.topic, opdta.payload)
            print("Opdta published.")
                       
            # Update order status
            self.control.set_order_state(self.site, order, OrderStates.RELEASED)
           
        else:
            print("No planned schedules found for assignment!")
               

    def do_show_schedule(self, arg):
        """Display the currently scheduled orders.
        
        The display may be restricted to specific orders or schedule
        states by giving the respective arguments (as keyword/value pair).
        
        Args:
            order (int):   order number (Optional).
            status (int):  status of scheduled record (Optional).
        """
        try:
            order = self._parse(arg)['order']
        except:
            order = None
        try:
            status = self._parse(arg)['status']
        except:
            status = None
           
        schedlist = self.control.get_schedule(self.site, order, status)
        tablspec = "{id:<8} {order:>10} {sfcu:>10} {operation:<15} {supplier:<6} {due:<10} {prio:^4} {statx:<10} {at:<12}"
        tablhead = {'id': 'Id', 'order': 'Order', 'sfcu': 'SFCU', 'operation': 'Operation', 'supplier': 'Suppl.', 'due': 'Due', 'prio': 'prio', 'statx': 'Status', 'at': 'at'}
        
        print(tablspec.format(**tablhead))
            
        for schedule in schedlist:          
            print(tablspec.format(**schedule))
 
    def do_show_orders(self, arg):
        """Display orders for a given status as a table.
        
        If no order state is given, all orders will be displayed.
        
        args:
            state (int):    Order state (optional).
        """
        
        orderlist = self.control.show_orders(**self._parse(arg))
        tablspec = "{site:<4} {id:<10} {variant:^20} {qty:>8} {unit:<4} {state:^5} {statx:<10}"
        tablhead = {'site': 'Site', 'id': 'Order Id', 'variant': 'Variant', 'qty': 'Qty', 'unit': 'Unit', 'state': 'State', 'statx': 'Status Text'}

        print(tablspec.format(**tablhead))
        
        for order in orderlist:
            print(tablspec.format(**order))  

    def do_show_param(self, arg):
        """Get list of parameter types of an order to be set.
        
        Args:
            order (int):    order number to be parameterized.
            mode (str):     optional: 'missing' or 'all'.
        """
        params = self.control.get_order_param(self.site, **self._parse(arg))
        
        for p in params:
            print(p.items())
    
    def do_prepare_opdta(self, arg):
        """ Populate the transfer objects for Shop Floor Control.
        
        TODO: solve problems in cerate_sfcu if wrong site is passed 

        
        Args:
            order (int):   Order number.
            variant (str): Variant code.
        """        
        self.control.new_opdta(**self._parse(arg))
        
    def do_publish_opdta(self, arg):
        """ Publish sfc order_context structure to mqtt server
        
        Args:
            order (int): Order number
            area (str):  Area code
        """
        opdta = self.control.get_opdta_msg(**self._parse(arg))
        self.control.publish(opdta.topic, opdta.payload)
        print("Published:", opdta.topic, opdta.payload)

    def do_set_param(self, arg):
        """Set missing parameters for a given order.
        
        Ask for input of missing order parameter values and set them if
        a value is given.
        
        Args:
            order (int): oder number to be parameterized.
            mode (str):  either 'missing' or 'all.        
        """
        params = self.control.get_order_param(self.site, **self._parse(arg))
        
        for p in params:
            ptyp = p['param_typ']
            pvalue = input("Enter parameter value for typ {}: ".format(ptyp))
            if pvalue:
                self.control.set_order_param(**self._parse(arg),
                                       param_typ=ptyp,
                                       param_value=pvalue)
                
    def do_create_sfcu(self, arg):
        rc = self.control.new_sfcu(self.site, **self._parse(arg))
        print(rc)
            
    def do_bye(self, arg):
        """Quit the application."""
        print('Thank you for using site:FUAS')
        self.close()
        return True  
    
    def close(self):
        # Stop the mqtt connection.
        print("Stopping mqtt connection ...")
        self.control.stop_connection(None)


#@profile
def main():
    """Main process for site control.
    
    Parse arguments, read configuration, assign database, instantiate SiteCmd 
    and start command loop.
    """
    # Parse and set runtime options
    parser = argparse.ArgumentParser(description='Wrapper for site_context. Implements the interactions of the order processing use cases.')
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
        config_file = config.get_conf_path('config_site.json')
    
    conf = config.get_config(config_file, 'Site')
    
    if args.database:  
        database = args.database
    else:
        database = config.get_db_path('site.db') 


    # Instantiate and start command loop.
    SiteCmd(conf, database).cmdloop()
    
    
if __name__ == '__main__':
    
    main()

    #===============================================================================
    # new_order(site=FUAS, material=FXF-1100, variant=col:blue, qty=2)
    # 
    # plan_order(site=FUAS, order=###)
    #  
    # release_order(order=###, area=area1)
    #===============================================================================
    
