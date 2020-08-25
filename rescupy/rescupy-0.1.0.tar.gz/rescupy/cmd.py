# -*- coding: utf-8 -*-
"""
Created on 2020-06-25

@author: Vincent Michaud-Rioux
"""

import numpy as np
import os
import shutil
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Cmd:
   """
   command class.
   
   Attributes
   ----------
   path : string
      Path to the rescu installation.

   mpi : string
      MPI-launcher command.

   Methods
   -------
   bs, dos, scf
      Perform the eponym calculations.
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):

      # required status
      reqDict = {
         "mpi" : False,
         "stdout": False,
         "path": False,
      }
      # default values
      defDict = {
         "mpi" : "mpiexec -n 1",
         "stdout": None,
         "path": None,
      }    

      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)

   def bs(self, file):
      command = self.get_bs_cmd()
      command(file)

   def dos(self, file):
      command = self.get_dos_cmd()
      command(file)

   def scf(self, file):
      command = self.get_scf_cmd()
      command(file)
      
   def find_rescu(self):
      if self.path is None or len(self.path) == 0:
         fpath = shutil.which("rescu_scf")
      else:
         fpath = self.path+"/rescu_scf"
      found = os.path.isfile(fpath) and os.access(fpath, os.X_OK)
      if (not found):
         raise NameError("Cannot find rescu binary "+fpath+
         ". You may remedy the situation calling Rescu.set_cmd({'path':'/path/to/rescu'}).")

   def get_bs_cmd(self):
      return self.get_cmd("bs")

   def get_dos_cmd(self):
      return self.get_cmd("dos")

   def get_scf_cmd(self):
      return self.get_cmd("scf")

   def get_cmd(self, name):
      self.find_rescu()
      command = self.mpi+" "
      if self.path is None or len(self.path) == 0:
         command = command+" rescu_"+name
      else:
         command = command+self.path+"/rescu_"+name
      if self.stdout is None:
         return lambda file: os.system(command+" -i "+file)
      else:
         return lambda file: os.system(command+" -i "+file+" >> "+self.stdout)

