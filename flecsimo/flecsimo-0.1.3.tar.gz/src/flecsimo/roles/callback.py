"""Mixin classes for mqtt callback handler.

Created on 22.06.2020

@author: Ralf Banning
"""
from json.decoder import JSONDecodeError

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

import sqlite3
import logging
from flecsimo.base import msg 
from flecsimo.base.states import AgentStates, ScheduleStates
from flecsimo.base.const import Facility
from flecsimo.roles.controller import PlanOperationsMixin, ProcureMixin, SchedulerMixin, TenderMixin

# TODO: find general convention for module log handler
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class EnrolMixin(object):
    """Callback handler for 'enrol' and 'quit' messages"""
    
    def on_enrol(self, client, userdata, message):
        pass

    def on_quit(self, client, userdata, message):
        pass


class RfqMixin(TenderMixin, object):
    """Callback handler for rfq (request for quote) messages.
    
    Both, areas and cells will publish a quotation, if they are running in 
    auto-mode and be able to supply the requested operations.
    """
        
    def on_rfq(self, client, userdata, message):
        """Read request for quote and persist.
        
        This functions defers requests for quote, storing them on a database
        and offers the service, if the operation is available at this level.
        (Does not imply that the service has to be active).
        
        Args:
            as requested by mqtt.Client interface
            
        Examples:
            rfg topic: "FUAS/area1/rfq"
            rfq payload : {"site": "FUAS", "sfcu": 21, "sender": "FUAS", "role": "DEMAND", "oplist": "27-DRILLING", "due": "2020-10-31", "prio": 0, "statx": "initial", "at": "2020-07-03T15:10"}
                       
        Note:
            See also https://stackoverflow.com/questions/19522505/using-sqlite3-in-python-with-with-keyword
        """     
        
        # TODO: implement on_rfq functionality
        
        pass
#===============================================================================
#         # Prepare SQL statements            
#         insert_schedule = """
#             INSERT or REPLACE INTO schedule
#                 (site, "order", sfcu, pds, operation, due, prio, state, statx, at)
#             VALUES (:site, :order, :sfcu, :pds, :operation, :due, :prio, :state, :statx, :at)"""          
# 
#         insert_quotation = """
#             INSERT or REPLACE INTO schedule
#                 (site, "order", sfcu, pds, operation, due, prio, state, statx, at)
#             VALUES (:site, :order, :sfcu, :pds, :operation, :due, :prio, :state, :statx, :at)"""          
#           
#         lookup_facility_operation = """
#             SELECT f.operation
#             FROM facility_operation AS f
#             JOIN task AS t ON f.operation = t.operation
#             AND CASE f.value_typ
#                     WHEN 'range' THEN t.param_value BETWEEN f.param_min and f.param_max
#                     WHEN 'value' THEN f.param_min = t.param_value
#                     ELSE 1
#                 END
#             WHERE t.site = :site
#             AND t."order" = :order
#             AND f.operation = :operation
#             """
# 
#         # Get request data from message 
#         rfq_msg = msg.as_dict(message.topic, message.payload)
#          
#         # Prepare request data for insert
#         #=======================================================================
#         # rfq_msg = rfq_msg.update({'state': ScheduleStates.REQUESTED.value, 
#         #                           'statx': ScheduleStates.REQUESTED.name})            
#         #=======================================================================
#      
#         conn = sqlite3.connect(self.database)
#         conn.row_factory = sqlite3.Row
#                      
#         
#         cur = conn.execute(lookup_facility_operation, {'operation': rfq_msg['spec']})  
#         r = cur.fetchone()
#          
#         if r:
#             # This is true, if service is available in database
#             # in this case we make an offer, otherwise ignore
#             # TODO: think of having also *active* service reported in database
#             # TODO: this is not yet a full implementation of oplist checking 
#             # TODO: rework. This is valid only for prototype.
#             demand = dict(r)
#  
#  
#              
#              
#             _log.info("Demand:", demand, "for sfcu:", rfq_msg['sfcu']) 
#              
#             quote = msg.Quote(self.sender, site=self.site, sfcu=rfq_msg['sfcu'])   
#              
#             try:
#                 with conn:
#                     conn.execute(insert_schedule) #TODO: parameters are missing
#                     conn.execute(insert_quotation, quote.dict)
#             except:
#                 raise       
#                        
#             _log.info("Send offer:", quote.payload) 
#             self.publish(quote.topic, quote.payload)
#              
#                      
#         else:
#             # TODO: there is no message type defined to propagate such a reject...
#             # TODO: rubbish, no entry into dsm, but status update of demand REQUESTED ->  REJECTED
#             _log.info("Requested demand", rfq_msg['spec'], "not deliverable. Reject request for sfcu", rfq_msg['sfcu'])
#       
#         conn.close()
#===============================================================================


class QuoteMixin(ProcureMixin, object):
    """Callback handler for 'quote' (quote for operations) messages."""
    
    def on_quote(self, client, userdata, message):
        
        # TODO: this is redundant in 'on_quote' and 'on_asgmtn'.
        insert_dsm_quotation = """
            INSERT INTO dsmbook (site, 'order', sfcu, party, role, scope, spec, due, prio, state, statx, at)
                SELECT site, :order, sfcu, :party, :role, :scope, :spec, due, prio, :state, :statx, :at
                FROM dsmbook
                WHERE site = :site
                AND sfcu=:sfcu
                AND role='DEMAND'"""         
        
        # sender, site=None, sfcu=None, scope=None, spec=None, state=None
        
        quote_msg = msg.as_dict(message.topic, message.payload)

        _log.info("\nReceived quotation:", quote_msg)

        try:
            site = quote_msg['site']
            order = quote_msg['order']
            party = quote_msg['party']
            # TODO: this is risky...(holds only for a cell quote):
            sfcu = quote_msg['sfcu']
            operation = quote_msg['spec']
        except:
            # TODO: execption handling for missing data.
            raise
                
        # Insert quotation into dsm_book              
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row

        with conn:
            conn.execute(insert_dsm_quotation, quote_msg)

        conn.close()

        # Immediate accept quotation in auto mode and send opdta
        if self.mode == 'AUTO':
                                       
            if self.typ == Facility.SITETYP:
                asgmt = self.get_asgmt()
                self.publish(asgmt.topic, asgmt.payload)
                
                opdta = self.get_opdta(self.sender, site, order, party) 
                               
                self.publish(opdta.topic, opdta.payload)
            
            elif self.typ == Facility.AREATYP:
                # TODO: Do things only Agents will do: start rfq to cell.
                asgmt = self.get_asgmt()
                self.publish(asgmt.topic, asgmt.payload)
                        
                opdta = self.get_opdta(self.sender, site, order, party, sfcu, operation)
                self.publish(opdta.topic, opdta.payload)
                
            else:
                _log.info("Wrong facility type: %s.", self.typ)
            

class AsgmtMixin(object):
    """Mixin class for assignment handling. 
    
    Assignments are the definite order to conduct operations in flecsimo.
    They will be published by site and area facilities and received by areas 
    and all kinds of cells.    
    """
    
    def on_asgmt(self, client, userdata, message):
        """ Callback handler for 'asgmt' (assignment of operations) messages
        
        This handler implements the receiver processes as used by area and cells:
        - Prepare the sql statement
        - Read and update the assignement message
        """
        # TODO: (Analyze) This sql-statement is duplicate to publisher.new_sechedule
        insert_or_replace_schedule = """
            INSERT or REPLACE INTO schedule
            VALUES (NULL, :site, :order, :sfcu, :pds, :operation, :supplier, :typ, :due, :prio, :state, :statx, :at)"""  
            
        # Get assignment data from message
        asgmt_msg = msg.as_dict(message.topic, message.payload)
        
        if asgmt_msg['supplier'] == self.myself:
               
            # Create new schedule.
            conn = sqlite3.connect(self.database)
            conn.row_factory = sqlite3.Row
        
            with conn:
                conn.execute(insert_or_replace_schedule, asgmt_msg)
            
            conn.close()
            
        else:
            #This will get relevant in RFQ-mode: discard any open quotes for that order/sfcu
            pass
        
        return

        
class OpdtaMixin(PlanOperationsMixin, ProcureMixin, SchedulerMixin, TenderMixin, object):
    """Mixin class for operation data messages.
    
    On receiving the operational data (opdta) the data will be checked 
    against assignment (hash, to be implemented). Only areas will either 
    assign operations contained in the opdta directly to a cell or 
    publish a request for quotation (rfq), if they are run in auto-mode. 
    The 
        schedule_operations(),
        choose_facility()
        assign_supplier() and
        request_quote() 
    
    function is provided in the roles.controller.ProcureMixin.
    """
    
    def on_opdta(self, client, userdata, message):
        """Callback handler for 'opdta' (operation data) messages
           
        This message handler store the operational data received. If agent 
        operates on area-level and set on AUTO mode, it will also plan for the
        operations to be executed for an sfcu and will either
        - choose a cell for operations execution -or-
        - issues an rfq message to start an offering process at cells side.
        
        Args:
            as requested by mqtt.Client interface
              
        Note:
            TODO: implement a hash value test for the received opdta.
            See also https://stackoverflow.com/questions/19522505/using-sqlite3-in-python-with-with-keyword
        """     
        # TODO: INSERT_OR_REPLACE is just a bypass for a unique constraint violation without "OR REPLACE" - find the reason for this!          
        insert_order = """
            INSERT OR REPLACE INTO 'order'  
            VALUES (:site, :id, :material, :variant, :qty, :unit, :pds, :at)"""
            
        insert_sfcu = """
            INSERT OR REPLACE INTO sfcu  
            VALUES (:site, :id, :order, :material, :state, :statx, :at)"""            

        insert_task = """
            INSERT OR REPLACE INTO task  
            VALUES (:site, :id, :order, :step, :next, :typ, :operation, :param_typ, :param_value, :pds_task)"""
              
        insert_part = """
            INSERT OR REPLACE INTO part  
            VALUES (:site, :task, :material, :usage, :qty, :unit)"""
              
        insert_resource = """
            INSERT OR REPLACE INTO resource 
            VALUES (:site, :task, :loc, :prio, :durvar, :durfix, :unit)"""
  
        # TODO: understand why this is necessary - deleting a opdta message in mqtt explorer issues an empty publish to that topic.
        # This leads an parsing exception in message instantiation-
        # Could be solved in msg base class or here. 
        try:
            opdta_msg = msg.as_dict(message.topic, message.payload)
            
        except JSONDecodeError as e:
            _log.info("Received non-valid opdta message. Skip message")
            _log.debug("Caught JSONDecodeError exception: {}".format(e))  
            return        
      
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row

        site = opdta_msg['data']['order'][0]['site']
        order = opdta_msg['data']['order'][0]['id']  

        
        with conn:
            conn.executemany(insert_order, opdta_msg['data']['order'])
            conn.executemany(insert_sfcu, opdta_msg['data']['sfcu'])
            conn.executemany(insert_task, opdta_msg['data']['task'])
            conn.executemany(insert_part, opdta_msg['data']['part'])
            conn.executemany(insert_resource, opdta_msg['data']['resource'])
        
        conn.close()
        
        if self.typ == Facility.AREATYP:
                
            if self.mode == 'AUTO':

                self.schedule_operations(site, order)

                facilitylist = self.choose_facility(site, order)
                               
                for facility in facilitylist:
                    
                    # TODO: (DD) Decide if assignment is always done on order level or should controlled on SFCU level
                    _log.debug("assign: site=%s, order=%s, supplier=%s and operation=%s", site, order, facility['facility'], facility['operation'])
                    self.assign_supplier(site, order, facility['facility'], facility['operation'])
                    
                asgmtlist = self.get_asgmt(self.sender, site, order)
                
                if asgmtlist:                         
                    for asgmt in asgmtlist:      
                        # Publish assignments (asgmt)
                        self.publish(asgmt.topic, asgmt.payload)
                        _log.info("Assignment for sfcu {} published.".format(asgmt.sfcu))    
                                         
                    # Bulk update schedule status
                    self.update_schedule(site, order, ScheduleStates.ASSIGNED)
                    
                    # Publish manufacturing instructions (opdta)                    
                    for facility in facilitylist:
                        opdta = self.get_opdta(self.sender, site, order, supplier=facility['facility'], operation=facility['operation'])
                        self.publish(opdta.topic, opdta.payload)
                        _log.info("Opdta published.")

                # TODO: This could be run in sub-mode 'AUTO-RFQ'
                # self.request_quote(site=site, order=order)   
        return
    
    def on_opcfm(self, client, userdata, message):
        """Callback handler for 'opcfm' (confirmation of opdta received) messages.
        
        TODO: implement 'on_opcfm' message handler.
        """
        pass


class ReportMixin(object):
    """Callback handler for 'opstat', 'reading' and 'logdta' messages."""
    
    def on_opstat(self, client, userdata, message):
        """Callback handler for 'opstat' messages.
        
        Updates operation state in various objects.

        TODO: implement 'on_opstat' message handler.        
        """
        pass
    
    def on_reading(self, client, userdata, message):
        """Callback handler for 'reading' messages.
        
        Stores or propagates readings from stations in a time-series db.
        
        TODO: implement 'on_reading' message handler.
        """
        pass

    def on_logdta(self, client, userdata, message):
        """Callback handler for 'logdta' messages.
        
        Stores or propagates log information to logging databases.

        TODO: implement 'on_logdta' message handler.
        """
        pass

    
class AgentstateMixin(object):
    """Callback handler for start and stop events.
    
    TODO: This is to be considered for redesign. It seems that the responsibilities
        for agentstate handling is not clear. It could be also in the executable
        module or in the connect module. The only reason it is located in this
        module is the fact, that the required base.msg dependencies already exists 
        here. 
    """

    def on_agentstart(self, client, userdata, flags, rc):
        """Publish agent state on startup.
        
        Note: this mixin should be bound to mqtt client.on_connect() callback handler. 
        """
        typ = self.typ.name
        
        _log.debug("Agent started. Sender=%s, typ=%s", self.sender, typ)
        
        self.agentstate = msg.Status(self.sender, typ, AgentStates.STARTED)    
        self.publish(self.agentstate.topic, self.agentstate.payload)
        
    def on_agentstop(self):
        """Publish agent state on agent stop.
        
        Note: this mixin should be bound to mqtt client.on_disconnect() callback handler. 
        """        
        typ = self.typ.name
        
        _log.debug("on_agentstop: send stop message for sender=%s, typ=%s", self.sender, typ)
        
        self.agentstate = msg.Status(self.sender, typ, AgentStates.STOPPED)
        self.publish(self.agentstate.topic, self.agentstate.payload)
