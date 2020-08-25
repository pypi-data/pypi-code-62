# -*- coding: utf-8 -*-
"""
Created on 2020-06-16

@author: Vincent Michaud-Rioux
"""

import h5py
import numpy as np
from math import pi
import scipy.io as sio
import re
import rescupy

def init_from_dict(self, reqDict, defDict, inpDict):
   """
   Initialize object from a dictionary.
   
   If certain attributes are themselves objects, init_from_dict is called recursively.

   Inputs
   ----------
   reqDict : dict
      Dict of keys and whether they are mandatory (True). If so, inpDict must contain 
      a non-trivial value.
   defDict : dict
      Dict of keys and their default values.
   inpDict : dict
      Dict of keys and user defined values.

   Return
   ----------
   self : generic object
      Object storing the attributes and values given by the inputs.

   """
   # Capitalize first letter of classes.
   # https://stackoverflow.com/questions/12410242/python-capitalize-first-letter-only
   fupper = lambda y: re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), y, 1)
   for key in defDict.keys():
      if key in inpDict or reqDict[key] is True:
         if not key in inpDict:
            raise NameError('Input dict is missing a value for parameter '+key+'.')
      if isinstance(defDict[key], dict):
         modpath = "rescupy."+key+"."+fupper(key)
         if key in inpDict:
            tmp = eval(modpath+"(inpDict['"+key+"'])")
         else:
            tmp = eval(modpath+"(defDict['"+key+"'])")
      else:
         if key in inpDict:
            tmp = inpDict[key]
         else:
            tmp = defDict[key]
      setattr(self, key, tmp)

def asdict(self):
   """
   Print generic object as a dictionary.
   
   If certain attributes are themselves objects, asdict is called recursively.
   """
   # init dict
   adict = {}
   # loop over attribute
   for key in self.__dict__.keys():
      # get attribute
      attr = getattr(self, key)
      # if it is a list, the first element should be representative, and hence
      # we see whether it is a rescu object (with asdict) or not
      if isinstance(attr, list):
         object_methods = [method_name for method_name in dir(attr[0])
                  if callable(getattr(attr[0], method_name))]
      # special treatment is we have an object list
      if isinstance(attr, list) and "asdict" in object_methods:
         adict[key] = [asdict_core(obj) for obj in attr]
         # adict[key] = adict[key]
      else:
         adict[key] = asdict_core(attr)
   return adict

def asdict_core(attr):
   """
   Print an attribute as a dictionary.
   """
   object_methods = [method_name for method_name in dir(attr)
               if callable(getattr(attr, method_name))]
   if "asdict" in object_methods:
      adict = attr.asdict()
   else:
      adict = attr
   if isinstance(adict, np.ndarray):
      adict = adict.flatten().tolist()
   return adict

def load_dcal(filename, varname=None):
   try:
      data = sio.loadmat(filename)
      data = data['data'][0]
      if not varname is None:
         data = data[varname][0]
      fmt = 'mat'
   except:
      data = h5py.File(filename, 'r')
      data = data['data']
      if not varname is None:
         data = data[varname]
      fmt = 'h5'
   if len(data) == 0:
      data = None
   return data, fmt

def load_dcal_var(data, varname, fmt, index):
   i = index
   if fmt == 'mat':
      if index is None:
         i = 0
      var = data[0][varname][i].squeeze()
   elif index is None:
      var = data[varname][0:].squeeze()
   else:
      var = data[data[varname][i][0]][0:].flatten()
   return var

def load_dcal_parameter(data, varname, fmt, index):
   i = index
   if fmt == 'mat':
      data = data[0]
      flds = list(data['Parameter'][i].dtype.names)
      if varname in flds:
         parameter = data['Parameter'][i][varname][0][0]
      else:
         parameter = None
   else:
      tmp = data[data['Parameter'][i][0]]
      flds = tmp.keys()
      if varname in flds:
         parameter = tmp[varname][0]
      else:
         parameter = None
   return parameter

def set_units(self, units):
   """
   Sets units to either atomic or si.
   """
   units = units.lower()
   if not units in ["atomic", "si"]:
      raise NameError("Unit system "+units+" not recognized.")
   for key in self.__dict__.keys():
      attr = getattr(self, key)
      object_methods = [method_name for method_name in dir(attr)
                  if callable(getattr(attr, method_name))]
      if "set_units" in object_methods:
         attr.set_units(units)
         setattr(self, key, attr)
         continue
      if len(key) < 5: 
         continue
      if key[-5:] != "Units":
         continue
      attr = getattr(self, key[:-5])
      unit = getattr(self, key)
      attr, unit = convert_units(attr, unit, units)
      setattr(self, key[:-5], attr)
      setattr(self, key, unit)

def convert_units(q, qUnits, units):
   """
   Convert quantity "q" with units "units" to system "units".
   """
   udict = get_units()
   qUnits = qUnits.lower()
   if qUnits in ["ang", "angstrom", "bohr"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "bohr"
      if units == "si": 
         newunit = "ang"
   elif qUnits in ["invang", "invbohr"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "invbohr"
      if units == "si": 
         newunit = "invang"
   elif qUnits in ["ev", "ha", "hartree"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "ha"
      if units == "si": 
         newunit = "ev"
   elif qUnits in ["ev/ang", "ha/bohr"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "ha/bohr"
      if units == "si": 
         newunit = "ev/ang"
   elif qUnits in ["ev/ang3", "ha/bohr3"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "ha/bohr3"
      if units == "si": 
         newunit = "ev/ang3"
   elif qUnits in ["invev", "invha"]:
      uq = udict[qUnits]
      if units == "atomic": 
         newunit = "invha"
      if units == "si": 
         newunit = "invev"
   else:
      raise NameError("Units dimension of "+qUnits+" not recognized.")
   if q is None:
      return q, newunit
   utarg = udict[newunit]
   if isinstance(q, list):
      q = [q0 * uq / utarg for q0 in q]
   else:
      q = q * uq / utarg
   return q, newunit

def read_field(filename, fieldname):
   """
   Read a field from an HDF5 file.

   Parameters: 
      filename (str): Path the the HDF5 file. For example, "rescu_scf_out.h5".

      fieldname (str): Path of the field in the HDF5 file. For example, "potential/effective".

   Returns: 
      fld (ndarray): 3D numpy array containing the field.
   """
   units = get_units()
   f = h5py.File(filename, mode='r')
   fld = f[fieldname][0:]
   fld = np.transpose(fld, [i for i in range(fld.ndim-1,-1,-1)])
   if re.match('potential', fieldname):
      fld = fld * units['ha']
   elif re.match('density', fieldname):
      fld = fld / units['bohr'] ** 3
   else:
      raise NameError('Unknown field type.')
   return fld

def get_units():
   """
   Function that creates a dictionary containing units.
   """
   # CODATA 2018 taken from
   # https://physics.nist.gov/cuu/Constants/index.html
   u = {"_c": 299792458.,            # Exact
         "_mu0": 4.0e-7 * pi,        # Exact
         "_grav": 6.67430e-11,       # +/- 0.000_15e-11
         "_hplanck": 6.62607015e-34, # Exact
         "_e": 1.602176634e-19,      # Exact
         "_me": 9.1093837015e-31,    # +/- 0.000_000_0028e-31
         "_mp": 1.67262192369e-27,   # +/- 0.000_000_000_51e-27
         "_nav": 6.02214076e23,      # Exact
         "_k": 1.380649e-23,         # Exact
         "_amu": 1.66053906660e-27}  # +/- 0.000_000_000_50e-27

   # derived from the CODATA values
   u["_eps0"] = (1 / u["_mu0"] / u["_c"]**2)  # permittivity of vacuum
   u["_hbar"] = u["_hplanck"] / (2 * pi)  # Planck constant / 2pi, J s

   u["ang"] = u["angstrom"] = 1.0
   u["nm"] = 10.0
   u["bohr"] = (4e10 * pi * u["_eps0"] * u["_hbar"]**2 /
               u["_me"] / u["_e"]**2)  # Bohr radius
   u["invang"] = 1. / u["ang"]
   u["invbohr"] = 1. / u["bohr"]

   u["ev"] = 1.0
   u["hartree"] = (u["_me"] * u["_e"]**3 / 16 / pi**2 /
                  u["_eps0"]**2 / u["_hbar"]**2)
   u["rydberg"] = 0.5 * u["hartree"]
   u["ry"] = u["rydberg"]
   u["ha"] = u["hartree"]
   # u["kj"] = 1000.0 / u["_e"]
   # u["kcal"] = 4.184 * u["kj"]
   # u["mol"] = u["_nav"]

   u["invev"] = 1.0 / u["ev"]
   u["invha"] = 1.0 / u["ha"]

   u["ev/ang"] = 1.0
   u["ha/bohr"] = 1.0 * u["ha"] / u["bohr"]

   u["ev/ang3"] = 1.0
   u["ha/bohr3"] = 1.0 * u["ha"] / (u["bohr"] ** 3)

   # u["second"] = 1e10 * sqrt(u["_e"] / u["_amu"])
   # u["fs"] = 1e-15 * u["second"]

   # u["kb"] = u["_k"] / u["_e"]  # Boltzmann constant, eV/K

   # u["pascal"] = (1 / u["_e"]) / 1e30  # J/m^3
   # u["gpa"] = 1e9 * u["pascal"]

   # u["debye"] = 1.0 / 1e11 / u["_e"] / u["_c"]
   # u["alpha"] = (u["_e"]**2 / (4 * pi * u["_eps0"]) /
   #             u["_hbar"] / u["_c"])  # fine structure constant
   # u["invcm"] = (100 * u["_c"] * u["_hplanck"] /
   #             u["_e"])  # cm^-1 energy unit

   # # Derived atomic units that have no assigned name:
   # # atomic unit of time, s:
   # u["_aut"] = u["_hbar"] / (u["alpha"]**2 * u["_me"] * u["_c"]**2)
   # # atomic unit of velocity, m/s:
   # u["_auv"] = u["_e"]**2 / u["_hbar"] / (4 * pi * u["_eps0"])
   # # atomic unit of force, N:
   # u["_auf"] = u["alpha"]**3 * u["_me"]**2 * u["_c"]**3 / u["_hbar"]
   # # atomic unit of pressure, Pa:
   # u["_aup"] = u["alpha"]**5 * u["_me"]**4 * u["_c"]**5 / u["_hbar"]**3

   # u["aut"] = u["second"] * u["_aut"]

   # # SI units
   # u["m"] = 1e10 * u["ang"]  # metre
   # u["kg"] = 1. / u["_amu"]  # kilogram
   # u["s"] = u["second"]  # second
   # u["a"] = 1.0 / u["_e"] / u["s"]  # ampere
   # # derived
   # u["j"] = u["kj"] / 1000  # Joule = kg * m**2 / s**2
   # u["c"] = 1.0 / u["_e"]  # Coulomb = A * s

   return u

def get_chemical_symbols():
   """Get a list of atomic species.

   Source
   -------
   Atomic Simulation Environment
   https://wiki.fysik.dtu.dk/ase/index.html
   commit 68f2a4c1e4c492654c32eb7e2bcd3a43a0dedf00 (origin/master, origin/HEAD, master)
   Merge: 22bbcf87e e13cd3184
   Author: Ask Hjorth Larsen <asklarsen@gmail.com>
   Date:   Tue May 5 17:08:04 2020 +0000
   """
   chemical_symbols = [
      # 0
      'X',
      # 1
      'H', 'He',
      # 2
      'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
      # 3
      'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
      # 4
      'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
      'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
      # 5
      'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
      'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
      # 6
      'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
      'Ho', 'Er', 'Tm', 'Yb', 'Lu',
      'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
      'Po', 'At', 'Rn',
      # 7
      'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
      'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
      'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
      'Lv', 'Ts', 'Og']
   return chemical_symbols