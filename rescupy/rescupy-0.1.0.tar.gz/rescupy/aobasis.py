# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.orb import AoOrb, KbOrb, RadFunc
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import load_dcal

class NaoBasis:
   """
   naoBasis class.
   
   Attributes
   ----------
   symbol : string
      Element symbol.
   path : string
      Pseudopotential path.
   orb : aoOrb-array
      Atomic orbitals.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict, varname):
      # default values
      defDict = {
         "path": None,
         "symbol": None,
      }
      # required status
      reqDict = {
         "path": True,
         "symbol": False,
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      filename = self.path
      data, fmt = load_dcal(filename)
      if fmt == 'mat':
         norb = len(data[varname][0][0])
      else:
         norb = len(data[varname]["Parameter"])
      self.orb = [AoOrb(filename, varname, index=i) for i in range(norb)]
      for snam, inam in zip(['symbol'],['symbol']):
         try:   
            if fmt == 'mat':
               tmp = data['atom'][0][0][inam][0][0]
            else:
               tmp = data['atom'][inam][0:]
               if inam == 'symbol':
                  tmp = ''.join(map(chr,tmp.flatten()))
            if isinstance(tmp, np.ndarray): tmp = float(tmp)
            if isinstance(tmp, np.str): tmp = str(tmp)
            setattr(self, snam, tmp)  
         except ValueError:
            raise NameError("Couldn't find parameter 'atom."+inam+" in file "+filename+".")

      self.finalize_init()

   def asdict(self):
      return utils_asdict(self)

   def finalize_init(self):
      self.numorb = len(self.orb)

class VnlBasis:
   """
   vnlBasis class.
   
   Attributes
   ----------
   symbol : string
      Element symbol.
   path : string
      Pseudopotential path.
   orb : aoOrb-array
      Atomic orbitals.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict, varname):
      # required status
      reqDict = {
         "path": True,
         "symbol": False,
      }
      # default values
      defDict = {
         "path": None,
         "symbol": None,
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      filename = self.path
      data, fmt = load_dcal(filename)
      norb = 0
      if fmt == 'mat' and len(data[varname][0]) > 0:
         norb = len(data[varname][0][0])
      elif len(data[varname]["Parameter"]) > 0:
         # find length based on HDF5 object reference
         norb = len(data[varname]["Parameter"])
      if varname == 'VnlSO':
         rng = range(1,norb)
      else:
         rng = range(0,norb)
      self.orb = [KbOrb(filename, varname, index=i) for i in rng] # 1st entry is empty
      for snam, inam in zip(['symbol'],['symbol']):
         try:   
            if fmt == 'mat':
               tmp = data['atom'][0][0][inam][0][0]
            else:
               tmp = data['atom'][inam][0:]
               if inam == 'symbol':
                  tmp = ''.join(map(chr,tmp.flatten()))
            if isinstance(tmp, np.ndarray): tmp = float(tmp)
            if isinstance(tmp, np.str): tmp = str(tmp)
            setattr(self, snam, tmp)  
         except ValueError:
            raise NameError("Couldn't find parameter 'atom."+inam+" in file "+filename+".")

      self.finalize_init()

   def asdict(self):
      return utils_asdict(self)

   def finalize_init(self):
      self.numorb = len(self.orb)
