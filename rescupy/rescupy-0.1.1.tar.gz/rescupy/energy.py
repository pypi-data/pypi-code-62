# -*- coding: utf-8 -*-
"""
Created on 2020-06-16

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import set_units as utils_set_units

class Energy:
   """
   energy class.
   
   Attributes
   ----------
   esr : float
      Short-range energy.
   ebs : float
      Band structure energy.
   edh : float
      Delta Hartree energy.
   exc : float
      Exchange-correlation energy.
   evxc : float
      Exchange-correlation potential energy.
   etot : float
      Total energy.
   efermi : float
      Fermi energy.
   evals : 3D array
      Kohn-Sham energies.
   frc : 2D array
      Atomic forces.
   
   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "esr"         : False,
         "esrUnits"    : False,
         "ebs"         : False,
         "ebsUnits"    : False,
         "edh"         : False,
         "edhUnits"    : False,
         "exc"         : False,
         "excUnits"    : False,
         "evxc"        : False,
         "evxcUnits"   : False,
         "etot"        : False,
         "etotUnits"   : False,
         "efermi"      : False,
         "efermiUnits" : False,
         "evals"       : False,
         "evalsUnits"  : False,
         "efree"       : False, 
         "efreeUnits"  : False, 
         "entropy"     : False, 
         "entropyUnits": False, 
         "frc"         : False,
         "frcUnits"    : False,
         "frcReturn"   : False,
         "stress"      : False,
         "stressUnits" : False,
         "stressReturn": False,
      }
      # default values
      defDict = {
         "esr"         : None,
         "esrUnits"    : "ev",
         "ebs"         : None,
         "ebsUnits"    : "ev",
         "edh"         : None,
         "edhUnits"    : "ev",
         "exc"         : None,
         "excUnits"    : "ev",
         "evxc"        : None,
         "evxcUnits"   : "ev",
         "etot"        : None,
         "etotUnits"   : "ev",
         "efree"       : None,
         "efreeUnits"  : "ev",
         "entropy"     : None,
         "entropyUnits": "ev",
         "efermi"      : None,
         "efermiUnits" : "ev",
         "evals"       : None,
         "evalsUnits"  : "ev",
         "frc"         : None,
         "frcUnits"    : "ev/ang",
         "frcReturn"   : False,
         "stress"      : None,
         "stressUnits" : "ev/ang3",
         "stressReturn": False,
      }    

      init_from_dict(self, reqDict, defDict, inpDict)

      if isinstance(self.evals, list): 
         self.evals = np.array(self.evals)
         
      if isinstance(self.frc, list): 
         self.frc = np.array(self.frc).reshape((-1,3))
         
      if isinstance(self.stress, list): 
         self.stress = np.array(self.stress).reshape((-1,3))
         
   def asdict(self):
      return utils_asdict(self)

   def set_units(self, units):
      return utils_set_units(self, units)
