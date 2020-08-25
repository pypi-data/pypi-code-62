# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

from scipy.interpolate import interp1d
from scipy.integrate import simps
import numpy as np
from rescupy.orb import RadFunc
from rescupy.pspot import Pspot
from rescupy.aobasis import NaoBasis
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Species:
   """
   species class.
   
   Attributes
   ----------
   label : string
      Species label (e.g. "Si1", "Au_surf").
   charge : float
      Electron charge.
   mass : float
      Atomic mass.
   magmom : float
      Magnetic moment (Cartesian).
   magrad : float
      Magnetic "radius" (for mag. moment integration).
   alphaZ : float
      Long-range energy correction (depends on unit cell volume).
   psp : float
      Pseudopotential.
   aob : float
      Atomic orbital basis.
   rna : float
      Neutral atom valence density (short-range).
   vna : float
      Neutral atom potential (short-range).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict):
      # required status
      reqDict = {
         "alphaZ": False,
         "charge": False,
         "label" : True ,
         "mass"  : False,
         "magmom": False,
         "magrad": False,
         "path"  : True,
      }
      # default values
      defDict = {
         "alphaZ" : None,
         "charge" : None,
         "label"  : "XX",
         "mass"   : None,
         "magmom" : 0.,
         "magrad" : 1.2,
         "path"   : None,
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      # do not update fields if they are found
      if not "psp" in inpDict.keys():
         inpDict["psp"] = {"path":get_path(inpDict)}
      elif not "path" in inpDict["psp"].keys():
         inpDict["psp"]["path"] = get_path(inpDict)
      self.psp = Pspot(inpDict["psp"])
      if not "aob" in inpDict.keys():
         inpDict["aob"] = {"path":get_path(inpDict)}
      elif not "path" in inpDict["aob"].keys():
         inpDict["aob"]["path"] = get_path(inpDict)
      self.aob = NaoBasis(inpDict["aob"], "OrbitalSet")
      self.rna = RadFunc(get_path(inpDict), "Rna")
      self.vna = RadFunc(get_path(inpDict), "Vna")
      self.alphaZ = calcAlphaZ(self.psp.vlc.rgrid, self.psp.vlc.rvals, self.psp.Z)
      if self.charge is None:
         self.charge = self.psp.Z

   def asdict(self):
      return utils_asdict(self)

def get_path(adict):
   if not "path" in adict.keys():
      raise NameError("Input file is missing a value for parameter species.path.")
   return adict["path"]

def calcAlphaZ(rr, vv, Z):
   # rr = spec.psp.Vlocal.rgrid
   # vv = spec.psp.Vlocal.rvals
   # Z = spec.psp.Z
   if rr[0] > 0.:
      tmp = interp1d(rr,vv, kind="cubic", fill_value="extrapolate")
      x = np.array([0.])
      rr = np.concatenate((x, rr))
      vv = np.concatenate((tmp(x), vv))
   integrand = rr ** 2 * vv + Z * rr
   return 4 * np.pi * simps(integrand,rr)
   