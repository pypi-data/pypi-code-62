# -*- coding: utf-8 -*-
"""
Created on 2020-06-16

@author: Vincent Michaud-Rioux
"""

import numpy as np
import h5py
from matplotlib import pyplot as plt
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import set_units as utils_set_units

class Dos:
   """
   dos class.
   
   Attributes
   ----------
   interval : 1D array
      Interval on which the DOS is calculated (e.g. [-5.5,8.1])
   resolution : float
      Grid resolution for the DOS interval

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "dos"             : False,
         "dosUnits"        : False,
         "efermi"          : False,
         "efermiUnits"     : False,
         "energy"          : False,
         "energyUnits"     : False,
         "interval"        : False,
         "intervalUnits"   : False,
         "lpdos"           : False,
         "orbA"            : False,
         "orbL"            : False,
         "orbM"            : False,         
         "pdos"            : False,
         "pdosUnits"       : False,
         "resolution"      : False,
         "resolutionUnits" : False,
      }
      # default values
      defDict = {
         "dos"             : None,
         "dosUnits"        : "invev",
         "efermi"          : None,
         "efermiUnits"     : "ev",
         "energy"          : None,
         "energyUnits"     : "ev",
         "interval"        : [-10.0, 10.0],
         "intervalUnits"   : "ev",
         "lpdos"           : False,
         "orbA"            : None,
         "orbL"            : None,
         "orbM"            : None,         
         "pdos"            : None,
         "pdosUnits"       : "invev",
         "resolution"      : 0.025,
         "resolutionUnits" : "ev",
      }    

      init_from_dict(self, reqDict, defDict, inpDict)

      for key in ["dos", "energy", "orbA", "orbL", "orbM", "pdos"]:
         attr = getattr(self, key)
         if isinstance(attr, list):
            setattr(self, key, np.array(attr))

      if isinstance(self.pdos, str):
         f = h5py.File(self.pdos, "r")
         self.pdos = f["dos"]["pdos"][0:].T

   def asdict(self):
      return utils_asdict(self)

   def plot_dos(self):
      x = self.energy
      y = self.dos
      fig = plt.figure()
      plt.plot(x, y, "-k")
      plt.xlabel("Energy ("+self.energyUnits+")")
      plt.ylabel("DOS ("+self.dosUnits+")")
      plt.show()
      return fig

   def plot_pdos(self, sumA=None, sumL=None, sumM=None):
      if sum([sumA is None, sumL is None, sumM is None]) > 1:
         NameError("User may not specify two sumX parameters.")
      x = self.energy
      y = self.dos
      fig = plt.figure()
      plt.plot(x, y, "-k")
      if all([sumA is None, sumL is None, sumM is None]):
         plt.show()
      else:
         y = self.pdos.reshape((x.size,-1), order='F')
         if sumA is None: sumA = [sumA]
         if sumL is None: sumL = [sumL]
         if sumM is None: sumM = [sumM]
         plot_pdos_core(x,y,[[self.orbA,sumA,"A"],[self.orbL,sumL,"L"],[self.orbM,sumM,"M"]])
      plt.xlabel("Energy ("+self.energyUnits+")")
      plt.ylabel("DOS ("+self.dosUnits+")")
      plt.show()
      return fig

   def set_units(self, units):
      return utils_set_units(self, units)

def plot_pdos_core(x, pdos, orbXXX):
   for a in orbXXX[0][1]:
      if a is None:
         orbA = np.ones_like(orbXXX[0][0], dtype=bool)
         labA = []
      else:
         orbA = orbXXX[0][0] == a
         labA = [orbXXX[0][2]," = ",str(a),","]
      for l in orbXXX[1][1]:
         if l is None:
            orbL = np.ones_like(orbXXX[1][0], dtype=bool)
            labL = []
         else:
            orbL = orbXXX[1][0] == l
            labL = [orbXXX[1][2]," = ",str(l),","]
         for m in orbXXX[2][1]:
            if m is None:
               orbM = np.ones_like(orbXXX[2][0], dtype=bool)
               labM = []
            else:
               orbM = orbXXX[2][0] == m
               labM = [orbXXX[2][2]," = ",str(m),","]
            orbX = np.logical_and(orbA, orbL)
            orbX = np.logical_and(orbX, orbM)
            d = np.sum(pdos[:,orbX], axis=1)
            label = "".join(labA+labL+labM)[0:-1]
            plt.plot(x, d,"-",label=label)
            plt.legend(loc="upper right")
