"""State classes for flecsimo objects.

Created on 21.03.2020

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
from enum import Enum

# TODO: define order_states in base.states


class DeviceStates(Enum):
    STOPPED = 0
    READY = 1
    STANDBY = 2
    SETUP = 3
    ACTIVE = 4
    DONE = 5
    HOLD = 6
    
class AgentStates(Enum):
    STOPPED = 0
    READY = 1
    SHUTDOWN = 3
    STARTED = 4
    
class ScheduleStates(Enum):
    INITIAL = 0
    PLANNED = 1
    REQUESTED = 2
    QUOTED = 3
    ASSIGNED = 4
    CONFIRMED = 5
    WIP = 6
    DONE = 7
    CANCELLED = 8
    REJECTED = 9
    FAILED = 10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

class OrderStates(Enum):
    INITIAL = 0
    CHECKED = 1
    PLANNED = 2
    RELEASED = 3
    CONFIRMED = 5
    WIP = 6
    DONE = 7
    CANCELLED = 8
    FAILED = 9

class SfcuStates(Enum):
    INITIAL = 0
    CHECKED = 1
    PLANNED = 2
    RELEASED = 3
    CONFIRMED = 5
    WIP = 6
    DONE = 7
    CANCELLED = 8
    FAILED = 9