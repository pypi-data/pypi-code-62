# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import copy
import numpy as np
from rescupy.orb import KbOrb, RadFunc
from rescupy.aobasis import VnlBasis
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import load_dcal

class Pspot:
   """
   pspot class.
   
   Attributes
   ----------
   symbol : string
      element symbol
   path : string
      pseudopotential path
   Z : integer
      pseudoion charge
   vlc : radFunc
      local pseudopotential
   rpc : radFunc
      partial core charge
   vnl : kbOrb-array
      KB-orbitals
   vso : kbOrb-array
      SO-orbitals

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict):
      # required status
      reqDict = {
         "path"  : True ,
         "symbol": False,
         "Z"     : False,
      }
      # default values
      defDict = {
         "path"  : None,
         "symbol": None,
         "Z"     : None,
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      filename = self.path
      self.vlc = RadFunc(filename, 'Vlocal')
      self.rpc = RadFunc(filename, 'Rpc')
      self.vnl = VnlBasis({"symbol":self.symbol, "path":self.path}, 'Vnl')
      self.vso = copy.deepcopy(self.vnl); self.vso.orb = self.vso.orb[0:1]; self.vso.numorb = 1
      # self.vso = VnlBasis({"symbol":self.symbol, "path":self.path}, 'VnlSO')
      data, fmt = load_dcal(filename)
      for snam, inam in zip(['Z','symbol'],['N','symbol']):
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

   def asdict(self):
      return utils_asdict(self)

         