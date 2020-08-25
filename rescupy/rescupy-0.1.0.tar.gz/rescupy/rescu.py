# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
import matplotlib.pyplot as plt
from rescupy.atomsys import AtomSys
from rescupy.cmd     import Cmd
from rescupy.solver  import Solver
from rescupy.kmesh   import increase_ksampling
from rescupy.utils   import asdict as utils_asdict
from rescupy.utils   import init_from_dict
from rescupy.utils   import read_field
from rescupy.utils   import set_units as utils_set_units
import json
import os 

class Rescu:
   """
   rescu class.
   
   Attributes
   ----------
   solver : solver object           
      Object containing solver related parameters.
   atomSys : atomSys object           
      Object containing atomSys related parameters.
   
   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict={}, filename=None):
      if not filename is None:
         self.read_output(filename, units="si")
         return

      # atomic system
      if not 'atomSys' in inpDict:
         NameError('"atomSys" parameters not found in input file.')
      self.atomSys = AtomSys(inpDict['atomSys'])

      # solver
      if 'solver' in inpDict:
         tmp = inpDict['solver']
      else:
         tmp = {}
      tmp = Solver(tmp)
      tmp.optim(self.atomSys)
      self.solver = tmp

      # rescu commands
      if 'cmd' in inpDict:
         tmp = inpDict['cmd']
      else:
         tmp = {}
      self.cmd = Cmd(tmp)

   def asdict(self):
      return utils_asdict(self)

   def conv_ksampling(self, etol=1e-2):
      if not "scfcmd" in self.__dict__.keys():
         NameError("Error in conv_ksampling: scfcmd not set. It can be set calling the set_cmd method.")
      basedict = self.asdict()
      detot = max(1., etol*10.)
      count = 0
      kref = self.atomSys.kmesh.grid; k1 = kref
      etot = []; kall = []
      print("%20s | %20s | %20s" % ("ksampling", "total energy (ev)", "delta energy (ev)"))
      while (abs(detot) > etol):
         hdf5file = "conv_ksampling_"+str(count)+".h5"
         jsonfile = "conv_ksampling_"+str(count)+".json"
         basedict["atomSys"]["kmesh"] = {"grid":k1, "gammaCentered":True}
         basedict["solver"]["restart"]["DMRPath"] = "conv_ksampling_"+str(count-1)+".h5"
         rscobj = Rescu(basedict)
         rscobj.write_input(jsonfile)
         rscobj.cmd.scf(jsonfile)
         os.system("mv rescu_scf_out.h5 "+hdf5file)
         os.system("mv rescu_scf_out.json "+jsonfile)
         rscobj.read_output(jsonfile)
         etot.append(rscobj.atomSys.energy.etot)
         kall.append(rscobj.atomSys.kmesh.grid)
         if count > 0:
            detot = etot[-1] - etot[-2]
         else:
            detot = etot[-1]
         print("%6d %6d %6d | %+20.8f | %+20.8f" % (k1[0], k1[1], k1[2], etot[-1], detot))
         k1 = increase_ksampling(k1, kref)
         count += 1
      detot = [e - etot[-1] for e in etot]
      print("%20s | %20s | %20s" % ("ksampling", "total energy (ev)", "energy error (ev)"))
      for i in range(0, len(etot)):
         print("%6d %6d %6d | %+20.8f | %+20.8f" % (kall[i][0], kall[i][1], kall[i][2], etot[i], detot[i]))

   def conv_resolution(self, etol=1e-2):
      if not "scfcmd" in self.__dict__.keys():
         NameError("Error in conv_resolution: scfcmd not set. It can be set calling the set_cmd method.")
      basedict = self.asdict()
      detot = max(1., etol*10.)
      count = 0
      res1 = self.atomSys.cell.lres
      etot = []; res = []
      print("%20s | %20s | %20s" % ("resolution (ang)", "total energy (ev)", "delta energy (ev)"))
      while (abs(detot) > etol):
         hdf5file = "conv_resolution_"+str(count)+".h5"
         jsonfile = "conv_resolution_"+str(count)+".json"
         basedict["atomSys"]["cell"]["grid"] = None
         basedict["atomSys"]["cell"]["lres"] = res1
         basedict["solver"]["restart"]["DMRPath"] = "conv_resolution_"+str(count-1)+".h5"
         rscobj = Rescu(basedict)
         rscobj.write_input(jsonfile)
         rscobj.cmd.scf(jsonfile)
         os.system("mv rescu_scf_out.h5 "+hdf5file)
         os.system("mv rescu_scf_out.json "+jsonfile)
         rscobj.read_output(jsonfile)
         etot.append(rscobj.atomSys.energy.etot)
         res.append(rscobj.atomSys.cell.lres)
         if count > 0:
            detot = etot[-1] - etot[-2]
         else:
            detot = etot[-1]
         print("%20.8f | %+20.8f | %+20.8f" % (res[-1], etot[-1], detot))
         res1 *= 0.9
         count += 1
      detot = [e - etot[-1] for e in etot]
      print("%20s | %20s | %20s" % ("resolution (ang)", "total energy (ev)", "energy error (ev)"))
      for i in range(0, len(etot)):
         print("%20.8f | %+20.8f | %+20.8f" % (res[i], etot[i], detot[i]))

   def plot_field(self, field, avg):
      """
      Plot the average of a field. 

      Parameters: 

         field (str): Path in the HDF5 filed pointed to by self.solver.restart.densityPath.

         avg (tuple): Length-2 tuple containing the axes along which to average the field.

      Returns:
         fig (figure): Pyplot figure showing the averaged field.  
      """
      if len(avg) != 2:
         raise NameError("Input avg must be of length 2.")
      if avg[0] == avg[1]:
         raise NameError("Input avg must have distinct entries.")
      axis = -1
      for d in range(3):
         if not d in avg:
            axis = d; break
      if not axis in [0,1,2]:
         raise NameError("Invalid input avg.")
      filename = self.solver.restart.densityPath
      field = read_field(filename, field)
      vavg = np.mean(field, axis=avg)
      x = self.atomSys.cell.get_grid(axis=axis)[:,axis]
      lx = self.atomSys.cell.get_length(axis=axis)
      fig = plt.figure()
      plt.plot(x, vavg)
      plt.xticks([0, lx])
      plt.grid(axis='x')
      plt.xlabel("position ("+self.atomSys.cell.avecUnits+")")
      plt.ylabel("field average (eV)")
      plt.show()
      return fig

   def set_units(self, units):
      return utils_set_units(self, units)

   def set_cmd(self, inpDict = {}):
      self.cmd = Cmd(inpDict)

   def write_input(self, filename, units="atomic"):
      self.set_units(units)
      adict = self.asdict()
      fid = open(filename, "w")
      json.dump(adict, fid, indent=2, sort_keys=True)
      fid.close()

   def read_output(self, filename, units="si"):
      fid = open(filename, "r")
      adict = json.load(fid)
      fid.close()
      self.__init__(adict)
      self.set_units(units)
