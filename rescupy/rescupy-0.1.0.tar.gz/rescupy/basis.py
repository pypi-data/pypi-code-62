# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Basis:
   """
   Basis class.
   
   Attributes
   ----------
   type : string
      Basis type (e.g. nao, pw).
   sprsthrs : float
      Sparsity threshold.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "type"    : False,
         "sprsthrs": False,
      }    
      # default values
      defDict = {
         "type"    : 'nao',
         "sprsthrs": 0.15,
      }    
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)