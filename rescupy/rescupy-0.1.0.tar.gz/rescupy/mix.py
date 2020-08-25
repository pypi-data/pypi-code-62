# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Mix:
   """
   mix class.
   
   Attributes
   ----------
   alpha : float
      Mixing parameter.
   imem : integer
      Mixer memory.
   maxit : integer
      Maximal number of self-consistent iterations.
   method : string
      Mixer algorithm.
   metric : string
      Mixer metric.
   precond : string
      Mixer preconditioner.
   tol : float
      Mixer tolerance.
   type : string
      Mixer type (e.g. density or potential).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "alpha" : False,
         "precond" : False,
         "metric" : False,
         "imem" : False,
         "method" : False,
         "tol" : False,
         "type" : False,
         "maxit" : False,
      }
      # default values
      defDict = {
         "alpha":0.2,
         "precond":"eye",
         "metric":"eye",
         "imem":20,
         "method":"pul",
         "tol":1E-8,
         "type":"den",
         "maxit":100
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)