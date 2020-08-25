# -*- coding: utf-8 -*-
"""
Created on 2020-05-12

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import set_units as utils_set_units

class Pop:
   """
   pop class.
   
   Attributes
   ----------
   type : string
      Occupancy scheme (e.g. Fermi-Dirac, Gaussian)
   blochl : logical
      Blochl correction in the tetrahedron scheme.
   mpn : integer
      Methfessel-Paxton scheme order.
   sigma : float
      Smearing parameter.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "type"      : False,
         "blochl"    : False,
         "mpn"       : False,
         "sigma"     : False,
         "sigmaUnits": False,
      }
      # default values
      defDict = {
         "type"      : "ga",
         "blochl"    : False,
         "mpn"       : 1,
         "sigma"     : 0.1,
         "sigmaUnits": "ev",
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      self.type = long2short(self.type)

      if not self.type in ['fx','fd','ga','mp','tm']: 
         raise NameError('Invalid pop.type value: '+self.type+'.')
      
      if self.type is 'fx':
         self.sigma = 0.0
         
      if not self.type is 'mp':
         self.mpn = 0
         
   def asdict(self):
      return utils_asdict(self)

   def set_units(self, units):
      return utils_set_units(self, units)

def long2short(long):
   if long == 'fixed':
      return 'fx'
   if long == 'fermi-dirac':
      return 'fd'
   if long == 'gauss':
      return 'ga'
   if long == 'methfessel-paxton':
      return 'mp'
   if long == 'tetrahedron':
      return 'tm'
   return long
