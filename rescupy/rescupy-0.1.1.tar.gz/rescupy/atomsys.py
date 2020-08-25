# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.atoms   import Atoms
from rescupy.cell    import Cell
from rescupy.dos     import Dos
from rescupy.energy  import Energy
from rescupy.kmesh   import Kmesh
from rescupy.pop     import Pop
from rescupy.species import Species
from rescupy.spin    import Spin
from rescupy.xc      import Xc
from rescupy.utils   import asdict    as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils   import set_units as utils_set_units
import scipy.io as sio
from matplotlib import pyplot as plt

class AtomSys:
   """
   atomSys class.
   
   Attributes
   ----------
   cell : cell object           
      Object containing cell related parameters.
   atoms : atoms object
      Object describing the atom collection (coordinates, species, etc.)
   kmesh : kmesh-object          
      Object containing kmesh related parameters.
   pop : pop-object 
      Object containing population (occupancy) related parameters.

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict):
      # required status
      reqDict = {
         "atoms"  : True,
         "cell"   : True,
         "dos"    : False,
         "energy" : False,
         "kmesh"  : False,
         "pop"    : False,
         "spin"   : False,
         "xc"     : False,
      }
      # default values
      defDict = {
         "atoms"  : {},
         "cell"   : {},
         "dos"    : {},
         "energy" : {},
         "kmesh"  : {},
         "pop"    : {},
         "spin"   : {},
         "xc"     : {},
      }

      init_from_dict(self, reqDict, defDict, inpDict)

      self.finalize_init()

      self.check_init()

   def asdict(self):
      return utils_asdict(self)

   def finalize_init(self):
      self.kmesh.set_bvec(self.cell)
      if self.kmesh.type == "line":
         self.kmesh.set_bz_lines(self.cell)

   def check_init(self):
      if (self.pop.type in ['tm'] and self.kmesh.grid == None):
         raise NameError('kmesh.grid must be provided if pop.type == "tm"')

      if (self.pop.type in ['tm'] and np.product(self.kmesh.grid) < 8):
         raise NameError('kmesh.grid must be at least 2 in every dimension if pop.type == "tm"')

   def plot_bs(self):
      evals = self.get_evals()
      evals = evals[:,:,0].T 
      # extract labels
      chpts = self.kmesh.checkPoints
      kpts = np.array(self.kmesh.kpts).reshape((-1,3))
      kpts = [kpts[k,:] for k in chpts]
      labels = self.kmesh.kpt_2_label(self.cell, kpts)
      # remove doublons (e.g. 'X' following 'X')
      for i in range(0, len(chpts)-1):
         if chpts[i] + 1 == chpts[i+1] and labels[i] == labels[i+1]:
            j = chpts[i]
            evals = np.delete(evals, j, axis=0)
            del chpts[i]
            del labels[i]
            for k in range(i, len(chpts)): chpts[k] = chpts[k] - 1
         if i + 2 >= len(chpts): break
      ef = np.ones(evals.shape[0]) * self.energy.efermi
      # plot
      fig = plt.figure()
      plt.plot(evals, "-b", label="_nolegend_")
      plt.plot(ef, "--k", label="Efermi")
      plt.legend(loc="upper right")
      plt.xlabel("BZ ("+self.kmesh.bvecUnits+")")
      plt.ylabel("Energy ("+self.energy.evalsUnits+")")
      plt.xticks(chpts, labels)
      plt.grid(axis='x')
      plt.show()
      return fig

   def set_units(self, units):
      return utils_set_units(self, units)

   def get_evals(self):
      nkpt = self.kmesh.get_kpts_num()
      nspin = self.spin.get_spin_num()
      evals = self.energy.evals
      if isinstance(evals, list):
         evals = np.array(evals)
      if isinstance(evals, np.ndarray): 
         evals = evals.reshape((-1,nkpt,nspin),order="F")
      return evals

   def get_vbm(self):
      evals = self.get_evals()
      lvals = evals < self.energy.efermi
      if np.all(lvals == lvals[:,0:1,0:1]):
         vbm = np.max(evals[lvals])
      else:
         vbm = None
      return vbm
