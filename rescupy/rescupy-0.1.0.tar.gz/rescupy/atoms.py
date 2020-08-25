# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
import scipy.io as sio
from rescupy.species import Species
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import get_chemical_symbols

class Atoms:
   """
   atoms class.
   
   Attributes
   ----------
   coords : 2D array    
      Atomic coordinates (fractional).
   species : species-array     
      Object containing species related parameters.
   speciesPtr : 1D array  
      Species index of each atom (atom <==> species correspondance).
   ionCharge : float
      Total ionic charge.
   valCharge : float
      Total valence charge.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict):
      # required status
      reqDict = {
         "coords": True,
         "speciesPtr": True,
         "valCharge": False,
         # "species": True,
      }
      # default values
      defDict = {
         "coords": None,
         "speciesPtr": None,
         "valCharge": None,
         # "species": {},
      }

      nspc = len(inpDict['species'])
      self.species = [Species(inpDict['species'][i]) for i in range(nspc)]
      
      init_from_dict(self, reqDict, defDict, inpDict)

      self.coords = np.array(self.coords).reshape((-1,3))
      self.speciesPtr = np.array(self.speciesPtr)
      self.ionCharge = sum(self.species[i].psp.Z for i in self.speciesPtr - 1)
      if self.valCharge is None:
         self.valCharge = self.ionCharge
      
      self.finalize_init()

   def asdict(self):
      return utils_asdict(self)

   def finalize_init(self):
      self.numspc = len(self.species)

   def get_positions(self, cell):
      return np.matmul(self.coords, cell.avec)

   def get_symbols(self, standard=False):
      if standard:
         symbols = [label_to_symbol(self.species[idx].label) for idx in self.speciesPtr - 1]
      else:
         symbols = [self.species[idx].label for idx in self.speciesPtr - 1]
      return symbols

def label_to_symbol(label):
   """Convert a label to an atomic species

   Parameters
   ----------
   label : str
      Should be an atomic species plus a tag. (e.g. H1, H_surf).

   Returns
   -------
   symbol : str
      The best matching species from the periodic table.

   Raises
   ------
   KeyError
      Couldn't find an appropriate species.

   """

   chemical_symbols = get_chemical_symbols()
   # two character species
   if len(label) >= 2:
      test_symbol = label[0].upper() + label[1].lower()
      if test_symbol in chemical_symbols:
         return test_symbol
   # one character species
   test_symbol = label[0].upper()
   if test_symbol in chemical_symbols:
      return test_symbol
   else:
      raise KeyError('Could not parse species from label {0}.'
                     ''.format(label))
