# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Mpidist:
   """
   mpi class.
   
   Attributes
   ----------
   grdblk : integer
      Grid blocking factor.
   kptblk : integer
      K-point blocking factor.
   orbblk : integer
      Orbital (matrices) blocking factor.
   bndblk : integer
      Band blocking factor.
   nrgblk : integer
      Energy blocking factor.
   imgblk : integer
      Image (NEB) blocking factor.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "bndblk": False,
         "bndprc": False,
         "grdblk": False,
         "grdprc": False,
         "imgblk": False,      
         "imgprc": False,      
         "kptblk": False,
         "kptprc": False,
         "nrgblk": False,
         "nrgprc": False,
         "orbblk": False,
         "orbprc": False,
      }    
      # default values
      defDict = {
         "bndblk": 4,
         "bndprc": None,
         "grdblk": 5,
         "grdprc": None,
         "imgblk": 1,
         "imgprc": None,      
         "kptblk": 1,
         "kptprc": None,
         "nrgblk": 1,
         "nrgprc": None,
         "orbblk": 32,
         "orbprc": None,
      }    
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)