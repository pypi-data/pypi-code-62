"""
Created on 30.05.2020

@author: Ralf Banning

Copyright and License Notice:

    flecsimo sfc processing
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
from flecsimo.base import msg


class EnrolMixin(object):
          
    def enrol(self, topic, payload):
        """Let an area join the site controller facilities.
    
        Args: 
            topic (str): Topic string.
            payload (str): Message payload in json format.        
    
        TODO: decide if cfmenrol is used or on publish should be
              enough to be evaluated (fire and forget or two-phase..)
              
        TODO: this currently has no real functionality - improve... 
    
        Scope: area and cell
        """
    
        enrol = msg.Enrol(self.sender, typ=None, desc=None, loc=None, oplist=None)
        
        return enrol

    def quit(self, topic, payload):
        """Announce quit of area operation to site control.
    
        TODO: decide if cfmquit is used or on publish should be
              enough to be evaluated (fire and forget or two-phase..)
    
        Scope: area and cell
        """
        pass
        