#!/usr/bin/env python3
"""
Device control based on python transitions library

Created on 17.03.2020

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
import sqlite3
import datetime

from flecsimo.base import config
from flecsimo.base import msg
from flecsimo.base.connect import Connector
from flecsimo.base.states import DeviceStates, ScheduleStates
from flecsimo.base.const import Facility
from time import sleep
from transitions import Machine
# from memory_profiler import profile
    
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())

class StationControl(object):
    """Main object handled by statemachine
    
    Note:
        could also inherit from Machine and Connector
    """

    def __init__(self, states, conf):
          
        # Get from config
        self.database = conf['database']
        self.site = conf['site']
        self.area = conf['area']
        self.cell = conf['cell']
        self.station = conf['station']
        self.broker = conf['broker']
        self.database = config.get_db_path(conf['database'])
        self.typ = Facility.STATIONTYP.value
        
        self.setup_tblspec = "{side:<6} {operation:<12} {param_typ:^10} {param_value:<10}"
        self.setup_tblhead = {'side': 'Change', 'operation': 'operation', 'param_typ': 'param.type', 'param_value': 'param.value'}

        # Derived values
        self.sender = msg.compose_topic(self.site, self.area, self.cell, self.station)
        self.myself = self.station 
        self.stnstat = msg.Status(self.sender, typ=self.typ, state=DeviceStates.STOPPED)
        
        # Start mqtt controller
        self.stnconn = Connector(cid=self.station)
        self.stnconn.start_connection()
        
        self.states = states
        
        self.transitions = [
            {'trigger': 'init', 'source': 'STOPPED', 'dest': 'READY'},
            {'trigger': 'proceed', 'source': ['READY', 'DONE', 'HOLD'], 'dest': 'STANDBY'},
            {'trigger': 'proceed', 'source': ['STANDBY', 'SETUP'], 'dest': 'ACTIVE', 'conditions': 'is_set_up'},
            {'trigger': 'proceed', 'source': 'STANDBY', 'dest': 'SETUP', 'unless': 'is_set_up'},
            {'trigger': 'proceed', 'source': 'ACTIVE', 'dest': 'DONE'},
            {'trigger': 'error', 'source': ['STANDBY', 'ACTIVE'], 'dest': 'HOLD'},
            {'trigger': 'stop', 'source': ['STANDBY', 'HOLD', 'STOPPED'], 'dest': 'STOPPED'},
        ]
        
        # Create state machine
        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial=DeviceStates.STOPPED.name,
            send_event=True,
            queued=True,
        )
    
        # Set state callbacks
        self.machine.on_enter_STOPPED('shut_down')
        self.machine.on_enter_READY('initialize')
        self.machine.on_enter_STANDBY('wait_for_sfcu')
        self.machine.on_enter_SETUP('set_up_operation')
        self.machine.on_enter_ACTIVE('start_operation')
        self.machine.on_enter_HOLD('wait_for_decission')
        self.machine.on_enter_DONE('complete_operation')
    
    # entry and exit functions
    def initialize(self, event):

        print("... initialize state machine.")
        self._publish_state_change(event)
        self.active_setup = {'operation': 'None', 'param_typ': 'None', 'param_value': 'None'}
        self.requested_setup = {'operation': 'None', 'param_typ': 'None', 'param_value': 'None'}
        self.proceed()
        
    def wait_for_sfcu(self, event):
        """Wait for shop floor control units."""
        
        self._publish_state_change(event)
         
        while True:
            sfcus = self._get_expected_sfcu()
            print("... expected sfcus:", sfcus)
            
            choice = input("... choose sfcu number: ")            
            sfcu = self._int_if_number(choice)
            
            if sfcu == "Q":
                self.stop()
                break

            elif sfcu in sfcus:
                try:
                    tasklist = self._get_task_by_sfcu(sfcu)
                    
                    sfcu=tasklist['sfcu']
                    
                    print("... received: {}".format(tasklist))                    
                    # Change state
                    self.proceed(**tasklist)
                    break
                               
                except:
                    # TODO: remainder of older concept - analyze if this makes sense in this way any more...
                    print("... sfcu", sfcu, "is unexpected. No operation is planned.")
                    e = " ".join(['Sfcu', sfcu, 'is unexpected.'])
                    self.error(error=e)
                    break
                
            else:
                print("... sfcu", sfcu, "is unexpected. Wait for new ASSIGNED schedules.")
                
    def set_up_operation(self, event):
        """Start operation set up process at station."""
        
        self._publish_state_change(event)
      
        #requested_operation = event.kwargs.get('operation')
        sfcu = event.kwargs.get('sfcu')
        setup_time = event.kwargs.get('setup')

        print("... set up operation\n")

        print("   ", self.setup_tblspec.format(**self.setup_tblhead))
        print("   ", self.setup_tblspec.format(side='From', **self.active_setup))
        print("   ", self.setup_tblspec.format(side='To', **self.requested_setup))
        print()
        
        self._simulate_processing(setup_time)
       
        self.active_setup = self.requested_setup
        
        self.proceed(sfcu=sfcu, **self.active_setup)
    
    def start_operation(self, event):
        """Start a manufacturing process step  for an SFCU at station."""
        
        self._publish_state_change(event)  
              
        sfcu = event.kwargs.get('sfcu')
        operation = event.kwargs.get('operation')
        param_typ = event.kwargs.get('param_typ')
        param_value = event.kwargs.get('param_value')
        processing_time = 15
        
        state = ScheduleStates.WIP.value
        statx = ScheduleStates.WIP.name
        
        sleep(0.2)
        print("... Start processing sfcu {} in operation {} with parameter {}: {}".format(sfcu, operation, param_typ, param_value))
        self._simulate_processing(processing_time)

        self._update_sfcu(sfcu, state, statx)

        self.proceed(sfcu=sfcu)
        
    def complete_operation(self, event):
        """Complete a manufacturing process step with unloading the product."""
        
        self._publish_state_change(event)
        
        sfcu = event.kwargs.get('sfcu')
        state = ScheduleStates.DONE.value
        statx = ScheduleStates.DONE.name
        
        while True:
            k = input("... enter 'U', if part is unloaded: ")
        
            if k == 'U':
                
                print("... completing sfcu", sfcu)               
                self._update_sfcu(sfcu, state, statx)
                
                self.proceed(event)
                break

    
    def wait_for_decission(self, event):
        
        self._publish_state_change(event)      
        
        decission = input("... press 'C' for continue, any other key will stop.")
        if decission == "C":
            self.proceed()
        else:
            self.stop()
    
    def shut_down(self, event):
        
        self._publish_state_change(event)
        
        self.stnstat.state = DeviceStates.STOPPED.value
        self.stnstat.descr = DeviceStates.STOPPED.name
        self.stnconn.publish(self.stnstat.topic, self.stnstat.payload)    
        self.stnconn.stop_connection(None)

    # conditions
    def is_set_up(self, event):
        
        self.requested_setup['operation'] = event.kwargs.get('operation')
        self.requested_setup['param_typ'] = event.kwargs.get('param_typ')
        self.requested_setup['param_value'] = event.kwargs.get('param_value')
              
        logging.info("active setup: {}\nrequested: {}".format(self.active_setup, self.requested_setup))
        
        if self.active_setup == self.requested_setup:
            logging.debug("Has to run setup")
            return True
        else:
            logging.debug("Is setup")
            return False
        
    # transition call backs
    def _publish_state_change(self, event):

        state = event.state.value.value  # for shure, that's not a typo!
        descr = event.state.name
        source = event.transition.source
        
        logging.info("entry/ %s --> (%s) %s, call: %s", source, state, descr, event.state.on_enter)    
        
        self.stnstat.state = event.state.value
        self.stnconn.publish(self.stnstat.topic, self.stnstat.payload)
        
    # Protected methods; accessing operations database
    def _get_task_by_sfcu(self, sfcu):
       
        select_task_by_sfcu = """
            SELECT s.id, s.sfcu, s.operation, t.param_typ, t.param_value, s.due, s.prio, o.setup
            FROM schedule s, task t, facility_operation o 
            WHERE s.operation = t.operation
            AND t.operation = o.operation
            AND t.param_typ = o.param_typ
            AND CASE o.value_typ
                    WHEN 'range' THEN t.param_value BETWEEN o.param_min and o.param_max
                    WHEN 'value' THEN o.param_min = t.param_value
                    ELSE 1
                END
            AND s.sfcu = :sfcu
            AND s.state = :state"""
                                 
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
               
        cur = conn.execute(select_task_by_sfcu, {'sfcu': sfcu, 'state': ScheduleStates.ASSIGNED.value})
        row = cur.fetchone()
        conn.close
        
        if row:
            tasklist = dict(row)
            _log.debug("tasklist: {}".format(tasklist))
        else:
            tasklist = None
            
        return tasklist
            

    def _get_expected_sfcu(self):
        
        select_next_operation = """
            SELECT sfcu
            FROM schedule
            WHERE state = :state"""
    
        state = ScheduleStates.ASSIGNED.value
        
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row  
                
        cur = conn.execute(select_next_operation, {'state': state})
        rows = cur.fetchall()
        sfcus = [ r['sfcu'] for r in rows]
        conn.close()
            
        return sfcus
    
    def _set_operation_state(self, sfcu):  
        
        update_operation_status = """UPDATE operation_status
                                     SET status = 'DONE'
                                     WHERE sfcu = :sfcu"""
        
        conn = sqlite3.connect(self.database)
        
        with conn:
            conn.execute(update_operation_status, {'sfcu': sfcu})
            
        conn.close()
        
    def _int_if_number(self, text):
        """Helper functions to convert string to int - if possible"""
        try:
            i = int(text)
        except:
            i = text
        return i
        
    def _update_sfcu(self, sfcu, state, statx):
        
        update_schedule = """
            UPDATE schedule
            SET state = :state,
                statx = :statx,
                at = :at
            WHERE site = :site 
            AND sfcu = :sfcu"""
            
        at = datetime.datetime.utcnow()

        conn = sqlite3.connect(self.database)
        try:
            with conn:
                conn.execute(update_schedule, {"site": self.site, 
                                               "sfcu": sfcu, 
                                               "state": state, 
                                               'statx': statx, 
                                               'at': at})          
        except:
            raise        
        conn.close()    
        
    def _simulate_processing(self, time):
        
        time = self._int_if_number(time)

        
        if time <= 60:

            print("    Processing time: {}s.".format(time))     
            print("    ", end="", flush=True)
            for _ in range(time):
                print("-", end="", flush=True)
            print("\n    ", end="", flush=True)
            for _ in range(time):
                print("|", end="", flush=True)
                sleep(1)
            print("\n", flush=True)

        else:
            print("    Processing time: {}s is more than 60s - will not progress bar shwon.".format(time))
            
        return 
    
# @profile(precision=4)
def main():

    print("""
    *************************************************************************
    * Welcome to the flecsimo station controller.                           *
    *                                                                       *
    * Copyright (C) 2020  Ralf Banning, Bernhard Lehner and Frankfurt       * 
    * University of Applied Sciences.                                       *
    * This program comes with ABSOLUTELY NO WARRANTY                        *
    *                                                                       *
    * Type help or ? to list commands.                                      *
    *                                                                       *
    *************************************************************************
    """
    )
    
    # Parse runtime options
    parser = argparse.ArgumentParser(description='Runs an station controller for manufacturing cells.')
    parser.add_argument('-c', '--config', help='Load configuration from file')
    parser.add_argument('--loglevel', help='Set log level as DEBUG, INFO, WANRING, ERROR or CRITICAL')
    parser.add_argument('--license', action='store_true', help='Show license and warranty disclaimer.')
    args = parser.parse_args()

    if args.license:
        print(license_text)
    
    if args.loglevel: 
        logging.basicConfig(level=args.loglevel)
    
    # Only warnings will be shown from state machine    
    logging.getLogger('transitions').setLevel(logging.WARNING)

    if args.config:  
        config_file = args.config
    else:
        config_file = config.get_conf_path('config_cell.json')
    
    conf = config.get_config(config_file, 'Cell')
     
    station_control = StationControl(DeviceStates, conf)
    
    print("Using database {}".format(station_control.database))

    k = input("Press Q to stop_connection, any other key will start_connection'\n")
    if k == 'Q':
        station_control.stop()
    
    else:
        station_control.init()
        print("Final state:", station_control.state.name)


if __name__ == '__main__':
    
    main()  
    
