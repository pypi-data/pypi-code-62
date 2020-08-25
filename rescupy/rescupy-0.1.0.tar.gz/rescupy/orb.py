# -*- coding: utf-8 -*-
"""
Created on 2020-05-12

@author: Vincent Michaud-Rioux
"""

import h5py
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import spherical_jn as jn
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import load_dcal, load_dcal_var, load_dcal_parameter

class RadFunc:
   """
   radFunc class.
   
   Attributes
   ----------
   funcid : 1D array
      Functional id (LibXC).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, filename, varname, index=0, ecut=36.75):

      if varname in ['Vna', 'Vlocal', 'Vnl', 'VnlSO']:
         vfld = "vvData"
      if varname in ['Rna', 'Rlocal', 'Rpc']:
         vfld = "rhoData"
      if varname in ['OrbitalSet']:
         vfld = "frData"

      if varname in ['Vna', 'Vlocal','Rna', 'Rlocal', 'Rpc']:
         i = None
      else: 
         i = index

      data, fmt = load_dcal(filename, varname)

      if data is None or len(data) == 0:
         self.rgrid = np.linspace(0, 5, 11)
         self.rwght = np.zeros((11))
         self.rvals = np.zeros((11))
         self.qgrid = np.linspace(0, 5, 11)
         self.qwght = np.zeros((11))
         self.qvals = np.zeros((11))
         self.ecut = max(self.qgrid)
         return
    
      self.rgrid = load_dcal_var(data, 'rrData', fmt, i)
      self.rwght = load_dcal_var(data, 'drData', fmt, i)
      self.rvals = load_dcal_var(data, vfld, fmt, i)

      try:
         self.qgrid = load_dcal_var(data, 'qqData', fmt, i)
         self.qwght = load_dcal_var(data, 'qwData', fmt, i)
         self.qvals = load_dcal_var(data, 'fqData', fmt, i)
      except:
         # self.qgrid, self.qwght = leggauss(int(ecut*10))
         # self.qgrid = (0 * (1 - self.qgrid) + ecut * (1 + self.qgrid)) / 2      
         nq = int(ecut*30)
         l = 0 if type(self) is RadFunc else self.l
         self.qgrid = np.linspace(0, ecut, num = nq + 1)
         self.qwght = np.ones((nq + 1)) / nq * ecut
         self.qwght[0] *= 0.5; self.qwght[-1] *= 0.5
         self.qvals = radialFT(self.rgrid, self.rwght, self.rvals, self.qgrid, l)

      self.ecut = max(self.qgrid)

   def asdict(self):
      return utils_asdict(self)

class Orb(RadFunc):
   def __init__(self, filename, varname, index=0, ecut=36.75):
      i = index
      data, fmt = load_dcal(filename, varname)
      try:
         tmp = load_dcal_parameter(data, 'L', fmt, i)
         self.l = int(tmp)
      except ValueError:
         raise NameError("Couldn't find parameter 'l' in file "+filename+".")
      self.n = -1
      super().__init__(filename, varname, index=index, ecut=ecut)

   def asdict(self):
      return utils_asdict(self)

class KbOrb(Orb):
   def __init__(self, filename, varname, index=0, ecut=36.75):
      i = index
      data, fmt = load_dcal(filename, varname)
      try:    
         tmp = load_dcal_parameter(data, 'halfLxEkbso', fmt, i)
         if tmp is None:
            tmp = load_dcal_parameter(data, 'KBenergy', fmt, i)
         self.kbnrg = float(tmp)
      except ValueError:
         raise NameError("Couldn't find parameter 'KBenergy' in file "+filename+".")
      self.energy = None
      self.kbcos = None

      super().__init__(filename, varname, index=index, ecut=ecut)

   def asdict(self):
      return utils_asdict(self)

class AoOrb(Orb):
   def __init__(self, filename, varname, index=0, ecut=36.75):
      i = index
      data, fmt = load_dcal(filename, varname)
      try:    
         tmp = load_dcal_parameter(data, 'Population', fmt, i)
         self.population = float(tmp)
      except ValueError:
         raise NameError("Couldn't find parameter 'Population' in file "+filename+".")
      self.zeta = -1
      self.energy = None
      self.coulombU = None
      self.exchangeJ = None

      super().__init__(filename, varname, index=index, ecut=ecut)

   def asdict(self):
      return utils_asdict(self)

def radialFT(r, fr, dr, q, l=0):
   """
   Description
   ----------
   Computes the radial Fourier transform.
   
   Parameters
   ----------
   r : 1D array
      Radial grid.
   fr : 1D array
      Radial values.
   dr : 1D array
      Radial integration weights.
   q : 1D array
      Fourier grid.
   l : 1D array
      Principal angular momentum.

   Returns
   ----------
   fq : 1D array
      Radial Fourier transform.
   """
   if l < 0:
      l = 0
   fq = r.reshape((-1,1)) * q.reshape((1,-1))
   fq = jn(l,fq)
   fq = r.reshape((-1,1)) ** 2 * fr.reshape((-1,1)) * fq
   fq = np.sqrt(2 / np.pi) * np.matmul(dr.reshape((1,-1)), fq).flatten()
   return fq
   # reference MATLAB code
   # fq = bsxfun(@times,r(:),q(:)');
   # fq = bsxfun(@times,r(:).^2.*fr(:),calcSphericalBessel(l,fq));
   # fq = sqrt(2/pi)*dr*fq;
 
