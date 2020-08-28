"""Role based methods for flecsimo order processing.

The classes within this module represent uses cases and wrap the 'methodful' roles 
within these. See the class documentation on details of these use cases.
 
Created on 25.05.2020

@author: Ralf Banning
"""


""" 
    Copyright and License Notice:

    flecsimo order processing
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
import datetime
import logging

from flecsimo.base.const import Facility
from flecsimo.base import msg
from flecsimo.base.states import OrderStates, SfcuStates, ScheduleStates

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


# TODO: move to base/exception module?
class NoResultException(Exception):
    """Exception thrown if an SQL selection return no rows unexpectedly."""
    pass


class OrderMixin(object):
    """Role methods for order processing.
    
    This class contains the methods for:
    - create an order
    - plan the order execution (which party 'does it')
    - release an order to a designated party.   
    """
    
    def new_order(self, site, material, qty=1, unit='PCE', variant=None):
        """Create a new order by manual data input.
        
        First checks if the data entered is processable. If true, it is checked 
        if parameter data has to be supplied and the order is inserted into the 
        database.
        
        An order is processable, if the following two condition are fulfilled:
        1. exactly one production-data-structure (pds) can be selected from the 
           database
        2. if the pds requires to select a variant, the variant argument have 
           to match one of these possible variants.
           
        If the order is processable but contains NULL values in the 
        pds_task.param_value column, the open_params counter signals that with
        a value > 1.
        
        Args:
            site (str):     identifier of the local site.
            material (str): material "number".
            qty (int):      number or quantity of items (default=1)
            unit (str):     unit of measure for qty (default=PCE)
            variant (str):  identifier for a variant to produce (default=None).
        
        Returns:   
            A 4-tupel (status:int, order:int, open_params:int, description:str) 
            where
            
            status = 0      order was processed successfuly,
            status = 1      number of pds records is 0 or >1 (error).
            status = 2      variant missing or does not match.
        """
        
        at = datetime.datetime.utcnow()
        
        # TODO: this selection does not respect time-slicing; therefore it would produce 'false positives'.
        check_pds = """
            SELECT count(pds.id) AS pdscount , 
                max(pds.has_variant) AS has_variant,
                max(pds.id) AS pds
            FROM pds 
            WHERE pds.material  = :material"""

        check_variant = """
            SELECT count(pds_task.variant) AS varcount
            FROM pds_task
            WHERE pds_task.pds = :pds
            AND pds_task.variant = :variant"""
            
        check_parameter = """
            SELECT count(DISTINCT pds_task.param_typ) AS pcount
            FROM pds_task
            WHERE pds_task.pds = :pds
            AND pds_task.param_typ IS NOT NULL
            AND pds_task.param_value IS NULL"""
        
        insert_order = """
            INSERT INTO 'order' 
                ("site", "material", "variant","qty","unit", "pds", "at")
            VALUES  
                (:site, :material, :variant, :qty, :unit, :pds, :at)"""            
        
        insert_order_status = """
            INSERT INTO order_status 
                ("site", "order", "state", "statx", "at", "actual_start", "actual_end", 
                "plan_start", "plan_end") 
            VALUES 
                (:site, :order, :state, :statx, :at, NULL, NULL, NULL, NULL);"""
                                                       
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
    
        with conn:
            cur = conn.cursor()
            
            cur.execute(check_pds, {'material': material})
            row = cur.fetchone()
            
            # Check if order data is processable
            # TODO: separate function?
            if row['pdscount'] != 1:
                rc = (1, None, None, "ERROR: either no or more than one pds found for material {}.".format(material))
                return(rc)
            else:
                pds = row['pds']
            
            if row['has_variant']:
                cur.execute(check_variant, {'pds': pds, 'variant': variant})
                res = cur.fetchone()
                
                if not res['varcount']:
                    rc = (2, None, None, "ERROR: variant {} does not match any known variant in pds.".format(variant))
                    return(rc)
            
            # check for missing parameters
            cur.execute(check_parameter, {'pds': pds})
            param = cur.fetchone()
            open_params = param['pcount']
            
            # Create new order record in database
            cur.execute(insert_order, {'site': site,
                                       'material': material,
                                       'variant': variant,
                                       'qty': qty,
                                       'unit': unit,
                                       'pds': pds,
                                       'at': at})
            order = cur.lastrowid
                    
            # TODO: use function 'set_order_state' instead?                      
            cur.execute(insert_order_status, {'site': site,
                                              'order': order,
                                              'state': OrderStates.INITIAL.value,
                                              'statx': OrderStates.INITIAL.name,
                                              'at': at})
               
        conn.close()
        
        rc = (0, order, open_params, "... Order {} created. Check for open params.".format(order))
        
        return(rc)
    
    def show_orders(self, state=None):
        """Get a list of orders with a status given.
        
        TODO: improve state handling.
        
        Args:
            state (int):    Order state.
        """  
        select_orders_by_state = """
            SELECT o.site, o.id, IFNULL(o.variant, '') AS variant, o.qty, o.unit, s.state, s.statx
            FROM "order"" as o, order_status AS s 
            WHERE s.state = :state
            AND s."order" = o.id"""
        
        select_all_orders = """
            SELECT o.site, o.id, IFNULL(o.variant, '') AS variant, o.qty, o.unit, s.state, s.statx  
            FROM "order" AS o, order_status AS s
            WHERE s."order" = o.id """ 
        
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
            
        with conn:
            if state == None:
                cur = conn.execute(select_all_orders)

            else:
                cur = conn.execute(select_orders_by_state, {'state': state})
        
            rows = cur.fetchall()
            orders = [ dict(r) for r in rows]
        conn.close()
        
        return orders    
    
    def set_order_param(self, site, order, param_typ, param_value):
        """Set missing parameters of tasks.
        
        Set the type and value of a task parameter for a given order and site.
        
        Args:
            site (str):       identifier of the loacel site.
            order (in):       oder number to be parameterized.
            param_type (str):  the parameter type to be set.
            param_value (str): a parameter value to be set.
        """       
                   
        insert_parameter = """
            INSERT OR REPLACE INTO order_parameter 
                ("order", "typ", "value")
            VALUES
                (:order, :param_typ, :param_value)"""   
               
        conn = sqlite3.connect(self.database)
     
        # TODO: exception handling
        try:
            with conn:          
                conn.execute(insert_parameter, {'order': order,
                                                'param_typ': param_typ,
                                                'param_value': param_value})            
            conn.close()
        except:
            pass 
    
    def get_order_param(self, site, order, mode='missing'):
        """List missing (or all) parameters of tasks.
        
        Selects tasks for a given operation which have parameter values
        declared. In mode "missing", only those with empty values
        will be returned, else all operation having parameter types.
        
        Args:
            site (str):    identifier of the local site.
            order (in):    order number to be parameterized.
            mode (str):    either 'missing' or 'all.
            
        Returns:
            A list of dictionaries of parameters.            
        """ 
        get_pds = """
            SELECT pds 
            FROM 'order' 
            WHERE 'order'.id  = :order"""
        
        select_missing_parameter = """
            SELECT DISTINCT param_typ
            FROM pds_task
            WHERE pds = :pds
            AND param_typ IS NOT NULL
            AND param_value IS NULL"""

        select_all_parameter = """
            SELECT DISTINCT param_typ
            FROM pds_task
            WHERE pds = :pds
            AND param_typ IS NOT NULL"""
    
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
     
        with conn:
            cur = conn.cursor()            
            cur.execute(get_pds, {'order': order})
            row = cur.fetchone()
            pds = row['pds']
            
            if mode == 'missing':
                cur.execute(select_missing_parameter, {'pds': pds})
            else:
                cur.execute(select_all_parameter, {'pds': pds})
            
            rows = cur.fetchall()
        conn.close()            
        
        return [dict(r) for r in rows]
    
    # @profile    
    def set_order_state(self, site, order, status):
        """Update order state."""

        # Prepare SQL statement        
        update_order_status = """
            UPDATE order_status
            SET state=:state, statx=:statx, at=:at
            WHERE "site" = :site 
            AND "order" = :order"""
            
        at = datetime.datetime.utcnow()

        try:
            state = status.value
            statx = status.name
        except:
            state = status
            statx = None
        
        # Execute on database            
        conn = sqlite3.connect(self.database)
            
        with conn:
            conn.execute(update_order_status, {'site': site,
                                               'order': order,
                                               'state': state,
                                               'statx': statx,
                                               'at': at})
        conn.close()      
    
    def new_opdta(self, site, order):
        """Prepare the operational data for an order as used by production cells.
        
        Make a parameterized copy of pds-structure linked to the order. If a
        variant is defined at order level, the respective pds subset will be
        selected.
               
        TODO: Test if all parameters are set (site and order).
        TODO: Consistent rc and exception handling -> design decision.
        
        Args:
            site (str):     identifier of the issuing, local site.
            order (int)     order number for which a pds copy should derived.
        """
        
        select_variant = """
            SELECT variant 
            FROM 'order'
            WHERE site = :site 
            AND id = :order"""
        
        #TODO: fix the fixed pt.pds=1 setting!!!
        insert_task = """
            INSERT INTO task 
                (site, id, 'order', step, next, typ, operation, param_typ, param_value, pds_task)
            SELECT :site, 
                NULL, 
                :order, 
                pds_task.step, 
                pds_task.next, 
                pds_task.typ, 
                pds_task.operation, 
                pds_task.param_typ, 
                pds_task.param_value, 
                pds_task.id  
            FROM pds_task, 'order'
            WHERE pds_task.pds = 'order'.pds
            AND 'order'.id = :order 
            AND (pds_task.variant IS NULL OR pds_task.variant = :variant)"""
            
        update_task_parameter = """
            WITH plist ('order', typ, value) AS  
                (SELECT * FROM order_parameter WHERE "order" = :order)
            UPDATE task
               SET param_value = (
                    SELECT plist.value
                    FROM plist
                    WHERE task.param_typ = plist.typ
                )
            WHERE "order" = :order
            AND param_typ in (SELECT typ FROM plist)"""
            
        insert_part = """
            INSERT INTO part
            SELECT :site, task.id, pds_part.material, pds_part.usage, pds_part.qty, pds_part.unit 
            FROM task, pds_part
            WHERE pds_part.pds_task = task.pds_task
            AND task.site = :site
            AND task."order" = :order"""   
            
        insert_resource = """
            INSERT INTO resource  
            SELECT :site,
                task.id, 
                pds_resource.loc,
                pds_resource.prio,
                pds_resource.durvar,
                pds_resource.durfix,
                pds_resource.unit
            FROM task, pds_resource
            WHERE pds_resource.pds_task = task.pds_task
            AND task.site = :site
            AND task."order" = :order"""        
            
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row
    
        try:
            with conn:
                # Get the variant
                cur = conn.execute(select_variant, {'site': site, 'order': order})
                row = cur.fetchone()
                variant = row['variant']
                
                # Create pds copy in database
                conn.execute(insert_task, {'site': site, 'order': order, 'variant': variant})
                conn.execute(update_task_parameter, {'order': order})
                conn.execute(insert_part, {'site': site, 'order': order})
                conn.execute(insert_resource, {'site': site, 'order': order})      
            conn.close()
            rc = (0, None)
        except Exception as e:
            rc = (1, e)
        
        return rc
    
    def get_pds(self, site, order):
        
        select_pds = """SELECT pds FROM "order" WHERE "id" = :order"""

        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row
        
        with conn:
            cur = conn.cursor()            
            cur.execute(select_pds, {'order': order})
            row = cur.fetchone()

        conn.close()
        
        return row['pds']
    
    def new_sfcu(self, site, order):
        """Split a given order into a set of shop floor control units (SFCUs).
        
        For a given order of 'n' items for a material 'm', this function 
        creates 'n' SFCU records for the material 'm' in the data base.
        
        TODO: derzeit keine Kontrolle über die Anzahl der SFCUs bei mehrfacher Ausführung - ändern!
        
        Args:
            site (str):     identifier for the local (issuing) site.
            order (int):    the order number to be split in to SFCUs.
            at (TIMESTAMP): the date/time as in the order.  
        """
        sfculist = []
    
        # TODO: use order_Stauts to prevent double creation of sfcus
        select_order = """
            SELECT 'order'.* 
            FROM 'order', order_status
            WHERE 'order'.site = :site 
            AND 'order'.id = :order
            AND 'order'.id = order_status.'order'
            AND order_status.state <= :state"""
            
        insert_sfcu = """
            INSERT INTO sfcu  
            VALUES (:site, NULL, :order, :material, :state, :statx, :at)"""
            
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row          
        
        try:
            with conn:
                # Get the order data    
                cur = conn.execute(select_order, {
                    'site': site,
                    'order': order,
                    'state': OrderStates.CHECKED.value})
                
                row = cur.fetchone()
                
                if row:
                    material = row['material']
                    qty = int(row['qty'])
                    at = row['at']
                else:
                    raise NoResultException                    
                
                # Create one sfcu per item quantity in database
                for _ in range(qty):
                    cur.execute(insert_sfcu, {'site': site,
                                              'order': order,
                                              'material': material,
                                              'state': SfcuStates.INITIAL.value,
                                              'statx': SfcuStates.INITIAL.name,
                                              'at': at})
                    # collect the new sfcu numbers for return list
                    sfculist.append(cur.lastrowid) 
                                                       
            conn.close
            
        except NoResultException: 

            _log.warning("Order {} is not in state 'initial' or 'checked'. Will not create any SFCU.".format(order))
       
        return sfculist    
                 
    def get_sfcu(self, site, order):
        """Get sfcus per order.
        
        Args:
            order(int):    order number.
        """
        
        select_sfcu_by_order = """
            SELECT id FROM sfcu WHERE site = :site AND "order" = :order"""
            
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
            
        with conn:
            cur = conn.execute(select_sfcu_by_order, {'site': site, 'order': order})       
            rows = cur.fetchall()    
            # sfculist = [r[0] for r in rows]
            sfculist = [r[0] for r in rows]
        conn.close()
        
        return sfculist


class SchedulerMixin(object):
    """Get or update information on demand and supply management."""
    
    def new_schedule(self, site, order, sfcu, pds, operation, supplier, typ, due, prio, state, statx):
        """ Manage content of demand an supply matching (dms).
        
        TODO: improve state handling
        TODO: habe a look on parameter list - it's to long!
        """
        insert_or_replace_schedule = """
            INSERT or REPLACE INTO schedule
            VALUES (NULL, :site, :order, :sfcu, :pds, :operation, :supplier, :typ, :due, :prio, :state, :statx, :at)"""  
           
        at = datetime.datetime.utcnow()
            
        conn = sqlite3.connect(self.database)
            
        with conn:
            cur = conn.execute(insert_or_replace_schedule, {'site': site,
                                                       'order': order,
                                                       'sfcu': sfcu,
                                                       'pds': pds,
                                                       'operation': operation,
                                                       'supplier': supplier,
                                                       'typ': typ,
                                                       'due': due,
                                                       'prio': prio,
                                                       'state': state,
                                                       'statx': statx,
                                                       'at': at})          
            schedule_id = cur.lastrowid
        conn.close()   
        
        return schedule_id     
       
    def get_schedule(self, site, order, status=None):
        """Get a schedule record for given criteria.
        
        Args:
            site (str):    Identifier for site.
            order (int):   Order id.
            statis(int):   Status id for schedule (optional)
        """       
        select_schedule = """
            SELECT id, 
                "order", 
                sfcu, 
                ifnull(operation, 'N/A') AS operation, 
                ifnull(supplier,'N/A') AS supplier, 
                ifnull(due, 'N/A') as due, 
                ifnull(prio, 0) AS prio, 
                statx, 
                at  
            FROM schedule
            WHERE site = :site
            AND CASE
                    WHEN :order IS NULL THEN 1
                    ELSE "order" = :order
                END
            AND CASE
                    WHEN :state IS NULL THEN 1
                    ELSE state = :state
                END"""
        
        try:
            state = status.value
        except:
            state = status
        
        conn = sqlite3.connect(self.database)       
        conn.row_factory = sqlite3.Row 
        
        _log.debug("site {}, order {}, state {}".format(site, order, state))
     
        with conn:
            cur = conn.cursor()       
            cur.execute(select_schedule, {'site': site, 'order': order, 'state': state })
            rows = cur.fetchall()
        conn.close()   
        
        return [dict(r) for r in rows]
    
    def update_schedule(self, site, order, status):
 
        # TODO: think of a better way to prepare statements with variable filters...
        update_schedule = """
            UPDATE schedule
            SET state = :state,
                statx = :statx,
                at = :at
            WHERE site = :site
            AND "order" = :order"""
                                
        at = datetime.datetime.utcnow()

        try:
            state = status.value
            statx = status.name
            
        except:
            state = status
        
        conn = sqlite3.connect(self.database)
        
        with conn:
            conn.execute(update_schedule, {'state': state,
                                            'statx': statx,
                                            'at': at,
                                            'site': site,
                                            'order': order})
            
        conn.close()


class PlanOperationsMixin(object):
    """Choose supplier for operations."""

    def schedule_operations(self, site, order):
        """Schedule the operations for scheduled sfcus."""
        
        insert_operation_schedule = """
            INSERT OR REPLACE INTO schedule
                ("site", "order", "sfcu", "pds", "operation", "due", "prio", "state", "statx", "at")
            SELECT s.site, s."order", s.sfcu, s.pds, t.operation, s.due, s.prio, :state, :statx, :at 
            FROM schedule as s, task as t
            WHERE s.site = :site 
            AND t.site = :site
            AND s."order" = :order
            AND t."order" = :order
            AND s.operation IS NULL
            AND statx = 'ASSIGNED'
            ON CONFLICT DO NOTHING"""
            
        state = ScheduleStates.INITIAL.value
        statx = ScheduleStates.INITIAL.name
        at = datetime.datetime.utcnow()
                
        conn = sqlite3.connect(self.database)
                
        with conn:
            conn.execute(insert_operation_schedule, {'site': site, 'order': order, 'state': state, 'statx': statx, 'at': at})
            
        conn.close()
        
        return
    
    def choose_facility(self, site, order):
        """Choose suppliers for each operation of a scheduled order.
        
        This is a simple "demo" implementation of a planning and optimizing 
        algorithm for selecting possible suppliers (cells) on base of a 
        supplier list (table facility_operation).
        
        Whenever the operation and task-parameters of an order matches with 
        a record in the facility_operation table, this record will be 
        selected. To avoid multiple suppliers to be selected for the same 
        operation, the supplier (cell) with the minimum setup time will be 
        chosen. When multiple cells have the same setup time for the same 
        operation, the cell with the lowest database rowid will be selected). 
        
        Note: this algorithm is not only simple, it's "over-simplifying":
        - it does not reflect the load of the cells.
        - it does not prevent from assigning multiple operations to the same 
          cell.
        - it works non predictive if two cells offer same set up time for the 
          same operation.
        """
        facilitylist = []
            
        select_facilities = """
            SELECT f.*
            FROM facility_operation AS f
            JOIN task AS t ON f.operation = t.operation
            AND CASE f.value_typ
                    WHEN 'range' THEN t.param_value BETWEEN f.param_min and f.param_max
                    WHEN 'value' THEN f.param_min = t.param_value
                    ELSE 1
                END
            WHERE t.site = :site
            AND t."order" = :order
            GROUP BY f.operation
            HAVING f.setup = min(f.setup)"""
                        
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
        
        with conn:
            cur = conn.cursor()       
            cur.execute(select_facilities, {'site': site, 'order': order})
            rows = cur.fetchall()
        conn.close()
        
        if rows:
            facilitylist = [dict(r) for r in rows]
        
        return facilitylist
    
    def assign_supplier(self, site, order, supplier, operation, sfcu=None):
        
        update_schedule_supplier = """
            UPDATE schedule
            SET supplier = :supplier,
                typ =  :typ,
                state = :state,
                statx = :statx,
                at = :at
            WHERE site =  :site
            AND "order" =  :order
            AND operation =  :operation
            AND CASE
                    WHEN :sfcu IS NULL THEN 1
                    ELSE sfcu = :sfcu
                END"""
            
        typ = Facility.CELLTYP.value
        state = ScheduleStates.PLANNED.value
        statx = ScheduleStates.PLANNED.name
        at = datetime.datetime.utcnow()
                    
        conn = sqlite3.connect(self.database)
                
        with conn:
            conn.execute(update_schedule_supplier, {'site': site,
                                                    'order': order,
                                                    'sfcu': sfcu,
                                                    'operation': operation,
                                                    'supplier': supplier,
                                                    'typ': typ,
                                                    'state': state,
                                                    'statx': statx,
                                                    'at': at})    
        conn.close()            

 
class ProcureMixin(object):  
    """Assign order processing tasks to other parties."""
    
    def get_asgmt(self, sender, site, order, sfcu=None):
        """Create assignment data ready to be published with mqqt
        
        TODO: create a hashvalue of the returned dictionary to be passed along with the 
            assignment message (see: https://docs.python.org/3/library/hashlib.html)   
            
        TODO: redesign ... this is very strange     
        
        Args: 
            site (str):    Identifier of the site that issues the demand.
            order (int):   Order number which is the reason for demand. 
            sfcu (int):    SFCU number - if None, all SFCUs for the given order will 
                           be selected.

        Returns:
            List of Asgmt objects to be published or None.
        """
        select_schedule = """
            SELECT site, "order", sfcu, pds, operation, supplier, typ, due, prio
            FROM schedule
            WHERE site = :site
            AND "order" = :order
            AND state = :state"""        
        
        asgmtlist = []
        
        # TODO: This is wrong:: site is not always sender
            
        conn = sqlite3.connect(self.database)       
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()
           
        with conn:    
               
            cur.execute(select_schedule, {'site': site, 'order': order, 'sfcu': sfcu, 'state': ScheduleStates.PLANNED.value })
            rows = cur.fetchall()
            
        conn.close()   
            
        schedule_list = [dict(r) for r in rows]
        
        for schedule in schedule_list: 
            
            schedule.update({'state': ScheduleStates.ASSIGNED})          
   
            # Build a list of asgmt message objects
            asgmtlist.append(msg.Asgmt(sender=sender, **schedule))
                  
        return asgmtlist
    
    def get_opdta(self, sender, site, order, supplier, sfcu=None, operation=None):
        """Select a complete opdta structure for given parameters."""
          
        select_order = """
            SELECT * 
            FROM 'order'
            WHERE site = :site
            AND id = :order"""  
    
        select_sfcus = """
            SELECT * 
            FROM sfcu 
            WHERE site = :site
            AND "order" = :order
            AND CASE 
                    WHEN :sfcu IS NULL THEN 1
                    ELSE id = :sfcu
                END"""     
                   
        select_tasks = """
            SELECT *
            FROM task
            WHERE site = :site
            AND "order" = :order
            AND CASE 
                    WHEN :operation IS NULL THEN 1
                    ELSE operation = :operation
                END"""
        
        select_parts = """          
            SELECT part.* 
            FROM part, task
            WHERE part.task = task.id
            AND task.site = :site
            AND task."order" = :order"""
        
        select_resources = """
            SELECT resource.*
            FROM resource, task
            WHERE resource.task = task.id
            AND task.site = :site
            AND task."order" = :order"""
            
        conn = sqlite3.connect(self.database)
        
        conn.row_factory = sqlite3.Row 
        
        # Select - create the single dictionary objects from the database
        # Note: The parsing was inspired by 'The Demz' in 
        # https://stackoverflow.com/a/18054751        
        try:
            cur = conn.execute(select_order, {'site': site, 'order': order})
            rows = cur.fetchall()
            order_data = [dict(r) for r in rows]
            
            cur = conn.execute(select_sfcus, {'site': site, 'order': order, 'sfcu': sfcu})
            rows = cur.fetchall()
            sfcu_data = [dict(r) for r in rows]
            
            cur = conn.execute(select_tasks, {'site': site, 'order': order, 'operation': operation})
            rows = cur.fetchall()
            task_data = [dict(r) for r in rows]
                
            cur = conn.execute(select_parts, {'site': site, 'order': order})
            rows = cur.fetchall()
            part_data = [dict(r) for r in rows]
            
            cur = conn.execute(select_resources, {'site': site, 'order': order})
            rows = cur.fetchall()
            resource_data = [dict(r) for r in rows]
                      
        except:
            # TODO: exception handlling.
            raise
            
        conn.close
        
        # Create the hierarchical dictionary
        opdta = msg.Opdta(sender=sender, receiver=supplier)
        opdta.data['order'] = order_data
        opdta.data['sfcu'] = sfcu_data
        opdta.data['task'] = task_data
        opdta.data['part'] = part_data
        opdta.data['resource'] = resource_data
        
        return opdta     

    
class TenderMixin(object):
    """Request quotes for order or sfcu execution from other parties."""
    
    def request_quote(self, site, order):
        """Select data for an rfq-message from dsmbook."""
               
        select_dsm = """
            SELECT site, "order", sfcu, role, scope, spec, due, prio
            FROM dsmbook
            WHERE site = :site
            AND "order" = :order
            AND role = 'DEMAND'"""
   
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
             
        cur = conn.execute(select_dsm, {"site": site, "order": order})
        
        rows = cur.fetchall()
                
        for row in rows:
            _log.debug("dict of row:", dict(row))
            
            rfq = msg.Rfq(self.sender, **dict(row))
            rfq.state = ScheduleStates.REQUESTED
            # TODO: set spec with required operation!
            
            self.publish(rfq.topic, rfq.payload)
            
        conn.close()     


class MasterDataMixin(object):
    """View or change flecsimo master data objects"""
    pass
