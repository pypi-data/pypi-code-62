# -*- coding: utf-8 -*-
"""
Created on 2020-06-16

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Restart:
   """
   restart class.
   
   Attributes
   ----------
   densityPath : string

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "densityPath": False,
         "DMkPath"    : False,
         "DMRPath"    : False,
      }    
      # default values
      defDict = {
         "densityPath": "",
         "DMkPath"    : "",
         "DMRPath"    : "",
      }    
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)