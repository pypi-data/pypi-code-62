# -*- coding: utf-8 -*-
"""
Created on 2020-05-12

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Spin:
   """
   spin class.
   
   Attributes
   ----------
   ispin : integer
      Spin treatment level (1 : degenerate, 2 : collinear, 4 : non-collinear).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "ispin": False,
      }
      # default values
      defDict = {
         "ispin": 1,
      }    

      init_from_dict(self, reqDict, defDict, inpDict)

      if not self.ispin in [1]: 
      # if not self.ispin in [1, 2, 4]: 
         raise NameError('Invalid spin.ispin value: '+self.ispin+'.')

   def asdict(self):
      return utils_asdict(self)

   def get_spin_num(self): 
      return 1