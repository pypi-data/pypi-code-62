# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.eig     import Eig
from rescupy.mpidist import Mpidist
from rescupy.mix     import Mix
from rescupy.basis   import Basis
from rescupy.restart import Restart
from rescupy.utils   import asdict as utils_asdict
from rescupy.utils   import init_from_dict

class Solver:
   """
   solver class.
   
   Attributes
   ----------
   basis : basis-object
      Deals with basis related parameters.
   eig : eig-object
      Deals with eigensolver related parameters.
   mix : mix-object
      Deals with mixer related parameters.
   mpi : mpi-object
      Deals with mpi related parameters.
   
   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "basis"   : False,
         "eig"     : False,
         "mix"     : False,
         "mpidist" : False,
         "restart" : False,
      }    
      # default values
      defDict = {
         "basis"   : {},
         "eig"     : {},
         "mix"     : {},
         "mpidist" : {},
         "restart" : {},
      }    
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)

   # optimize solver parameters based on atomSys object
   def optim(self, sobj):
      nval = sobj.atoms.valCharge
      # fix number of target bands
      if self.eig.trgtband is None:
         self.eig.trgtband = [1, int((nval + 1) // 2) + 8]
      # fix number of included bands
      if self.eig.inclband is None:
         self.eig.inclband = [1, int((nval + 1) // 2) + 8]
