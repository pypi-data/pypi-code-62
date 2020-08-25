# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.cell    import bra2avec
from rescupy.utils   import asdict as utils_asdict
from rescupy.utils   import init_from_dict
from rescupy.utils   import set_units as utils_set_units

class Kmesh:
   """
   kmesh class.
   
   Attributes
   ----------
   bvec : 2D array
      Reciprocal unit kmesh row-vectors
   kpts : 2D array
      k-points in fractional coordinates
   kwght : 1D array
      k-points weights

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):

      # required status
      reqDict = {
         "bvec"         : False,
         "bvecUnits"    : False,
         "checkPoints"  : False,
         "gammaCentered": False,
         "grid"         : False,
         "kpts"         : False,
         "kwght"        : False,
         "type"         : False,
      }
      # default values
      defDict = {
         "bvec"         : None,
         "bvecUnits"    : "invang",
         "checkPoints"  : None,
         "gammaCentered": False,
         "grid"         : None,
         "kpts"         : None,
         "kwght"        : None,
         "type"         : "full",
      }  

      init_from_dict(self, reqDict, defDict, inpDict)

      if not self.grid is None and self.kpts is None:
         if self.type == "full": 
            kpts = monkhorst_pack(self.grid)
            if self.gammaCentered:
               shift = np.array(self.grid)
               shift = np.mod(shift + 1, 2) / 2. / shift
               kpts = kpts + shift.reshape((-1,3))
            self.kpts = kpts
            nkpt = np.prod(self.grid)
            self.kwght = np.ones(nkpt) / nkpt

      if not self.kpts is None and len(self.kwght) < len(self.kpts) / 3:
         raise NameError('kwght and kpts have incompatible dimensions.')

      if not self.kwght is None and not np.isclose(1., np.sum(self.kwght)):
         raise NameError('kwght does not sum to 1.')

      if isinstance(self.kpts, list):
         self.kpts = np.array(self.kpts).reshape((-1,3))

   def asdict(self):
      return utils_asdict(self)

   def get_kpts_num(self):
      if isinstance(self.kpts, list):
         nkpt = len(self.kpts) // 3
      elif isinstance(self.kpts, np.ndarray):
         nkpt = self.kpts.shape[0]
      else:
         raise NameError('Invalid type for attribute kpts.')
      return nkpt

   def get_bz_dist(self, kpt0, kpt1):
      dist = np.matmul(kpt1 - kpt0, self.bvec)
      return np.linalg.norm(dist)

   def get_bz_segment(self, kpt0, kpt1, n = None, res = None):
      if n is None and res is None:
         NameError("n or res must be specified.")
      if not n is None:
         kpts = np.zeros((n, 3))
         kpts[:,0] = np.linspace(kpt0[0], kpt1[0], n)
         kpts[:,1] = np.linspace(kpt0[1], kpt1[1], n)
         kpts[:,2] = np.linspace(kpt0[2], kpt1[2], n)
      else: 
         dist = self.get_bz_dist(kpt0, kpt1)
         n = np.ceil(dist / res).astype(int)
         kpts = self.get_bz_segment(kpt0, kpt1, n = n)
      return kpts

   def kpt_2_label(self, cell, kpts):
      if cell.bravais is None:
         cell.bravais = cell.get_bravais_lattice()
      bravais = cell.bravais
      avec = cell.avec
      avecStd = cell.get_standard_lattice()
      pmat = np.matmul(avecStd, np.linalg.inv(avec)).transpose()
      labels = []
      for i in range(0, len(kpts)):
         k = np.matmul(kpts[i],pmat)
         labels.append(kValue2kSymbol(bravais, avecStd, k))
      return labels

   def set_units(self, units):
      return utils_set_units(self, units)

   def set_bvec(self, cell):
      self.bvec, self.bvecUnits = cell.reciprocal()

   def set_bz_lines(self, cell):
      if not self.kpts is None:
         return
      if cell.bravais is None:
         cell.bravais = cell.get_bravais_lattice()
      bravais = cell.bravais
      avec = cell.avec
      avecStd = cell.get_standard_lattice()
      pmat = np.matmul(avec, np.linalg.inv(avecStd)).transpose()
      # define checkpoints
      if self.checkPoints is None:
         checkPoints = defaultSymmetryKPoints(bravais, avecStd)
      else:
         checkPoints = self.checkPoints
      # get line segments
      checkPoints = split_bz_lines(checkPoints)
      # convert to numerical format
      for i in range(0, len(checkPoints)):
         kpt0 = kSymbol2kValue(bravais, avecStd, checkPoints[i][0]) # checkPoint returned as is if not a str
         if isinstance(checkPoints[i][0], str): kpt0 = np.matmul(kpt0,pmat)
         kpt1 = kSymbol2kValue(bravais, avecStd, checkPoints[i][1]) # checkPoint returned as is if not a str
         if isinstance(checkPoints[i][1], str): kpt1 = np.matmul(kpt1,pmat)
         checkPoints[i] = [kpt0, kpt1]
      # get total length
      klen = 0.0
      for i in range(0, len(checkPoints)):
         kpt0 = checkPoints[i][0]
         kpt1 = checkPoints[i][1]
         klen += self.get_bz_dist(kpt0, kpt1)
      # get resolution
      if not self.grid is None:
         res = klen / self.grid
      else:
         res = 0.015
      # interpolate between checkpoints to obtain segments
      kpts = np.zeros((0,3))
      count = 0; checkIndex = np.zeros(2*len(checkPoints)).astype(int)
      for i in range(0, len(checkPoints)):
         kpt0 = checkPoints[i][0]
         kpt1 = checkPoints[i][1]
         ktmp = self.get_bz_segment(kpt0, kpt1, res = res)
         kpts = np.concatenate((kpts, ktmp), axis = 0)
         checkIndex[2*i] = count
         checkIndex[2*i+1] = count + ktmp.shape[0] - 1
         count = checkIndex[2*i+1] + 1
      self.kpts = kpts
      nkpt = kpts.shape[0]
      self.kwght = [1. / nkpt for i in range(nkpt)]
      self.grid = [nkpt]
      self.checkPoints = checkIndex

####################
# module functions #
####################

def monkhorst_pack(grid):
   kx = monkhorst_pack_nodes(grid[0])
   ky = monkhorst_pack_nodes(grid[1])
   kz = monkhorst_pack_nodes(grid[2])
   kx, ky, kz = np.meshgrid(kx, ky, kz, indexing='ij')
   kpts = np.hstack((kx.reshape((-1,1), order='F'), 
                     ky.reshape((-1,1), order='F'), 
                     kz.reshape((-1,1), order='F')))
   return kpts

def monkhorst_pack_nodes(n):
   k = np.linspace(0., 1., num=n+1)[0:n]
   if (n % 2 == 0):
      k += .5 / n
   k -= np.round(k)
   return k

def split_bz_lines(checkPoints):
   if not isinstance(checkPoints[0], list):
      return split_list(checkPoints)
   newlist = []
   for i in range(0, len(checkPoints)):
      newlist = newlist+split_list(checkPoints[i])
   return newlist
         
def split_list(alist):
   newlist = []
   for i in range(0, len(alist) - 1):
      newlist.append(alist[i:i + 2])
   return newlist

def increase_ksampling(k, kref):
   k0 = k
   kw = np.array(kref).astype(float)
   while all([a >= b for a, b in zip(k0, k)]):
      kw *= 1.1
      k = np.round(kw).astype(int).tolist()
   return k

def defaultSymmetryKPoints(crystalStructure, avecStd):
   """
   Return a linear BZ sampling given the crystal structure and lattice vectors.

   Parameters
   ----------
   crystalStructure : string
      Name of the Bravais lattice.

   avecStd : 2D array
      3 x 3 array of row-vectors corresponding to the lattice vectors in the standard 
      ordering (AFLOW).

   Returns
   -------
   symmetryKPoints : list of strings
      Path of high-symmetry k-point labels.

   Author Info:
   Lei Liu, HZWTech
   2015-10
   Vincent Michaud-Rioux
   2020-06-23
   """

   avecStd = avecStd.transpose() # here primitiveCellVectors = [a1 a2 a3]
   epsilon = 1e-3
   if crystalStructure.lower() in ["cubic", "cub", "simplecubic", "sc", "cp"]:
      # 1: ucv = pcv = [[1 0 0]', [0 1 0]', [0 0 1]']
      # symmetryKPoints = [["G","X","M","G","R","X"],["M","R"]]
      symmetryKPoints = [["G","X","M","G","R","X"],["M","R"]]
      # ["G", "X", "M", "G", "R", "X"] ["M", "R"]
   elif crystalStructure.lower() in ["facecenteredcubic", "fcc", "cf"]:
      # 2: pcv = [[0 1./2. 1./2.]', [1./2., 0, 1./2.]', [1./2. 1./2. 0]']
      #    ucv = [[1 0 0]', [0 1 0]', [0 0 1]']
      # symmetryKPoints = ["U","X","G","X","W","K","G","L","U","W","L","K"]
      symmetryKPoints = [["G","X","W","K","G","L","U","W","L","K"],["U","X"]]
      # ["G","X","W","K","G","L","U","W","L","K"] ["U","X"]
   elif crystalStructure.lower() in ["bodycenteredcubic", "bcc", "ci"]:
      # 3: pcv = [[-1./2. 1./2. 1./2.]', [1./2., -1./2., 1./2.]', [1./2. 1./2. -1./2.]']
      #    ucv = [[1 0 0]', [0 1 0]', [0 0 1]']
      # symmetryKPoints = [["G","H","N","G","P","H"] ["P","N"]]
      symmetryKPoints = [["G","H","N","G","P","H"],["P","N"]]
      # ["G","H","N","G","P","H"] ["P","N"]
   elif crystalStructure.lower() in ["tetragonal", "tet", "tp"]:
      # 4: ucv = pcv = [[1 0 0]', [0 1 0]', [0 0 5]']
      # symmetryKPoints = [["G", "X", "M", "G", "Z", "R", "A", "Z"] ["X", "R", "G", "A", "M"]]
      symmetryKPoints = [["G","X","M","G","Z","R","A","Z"],["X","R"],["M","A"]]
      # ["G", "X", "M", "G", "Z", "R", "A", "Z"] ["X", "R"]  ["M", "A"]
   elif crystalStructure.lower() in ["bodycenteredtetragonal", "bct", "ti"]:
      # 5: pcv = [[-1./2. 1./2. 5/2]', [1./2., -1./2., 5/2]', [1./2. 1./2. -5/2]']
      #    ucv = [[1 0 0]', [0 1 0]', [0 0 5]']
      pcv4bcc = np.array([[-1./2.,1./2.,1./2.], [1./2., -1./2., 1./2.], [1./2., 1./2., -1./2.]]).transpose()
      ucv4bcc = np.eye(3)
      pcv = avecStd
      ucv = pcv*(np.linalg.inv(pcv4bcc)*ucv4bcc)
      if np.norm(ucv[:,2]) < np.norm(ucv[:,0]):
         type = "1"
      else:
         type = "2"
      if type is "1":
         # symmetryKPoints = ["X", "P", "G", "X", "M", "G", "Z", "P", "N", "Z1", "M"]
         symmetryKPoints = [["G","X","M","G","Z","P","N","Z1","M"],["X","P"]]
         # ["G", "X", "M", "G", "Z", "P", "N", "Z1", "M"] ["X", "P"]
      elif type is "2":
         # symmetryKPoints = ["X", "P", "G", "X", "Y", "S", "G", "Z", "S1", "N", "P", "Y1", "Z"]
         symmetryKPoints = [["G","X","Y","S","G","Z","S1","N","P","Y1","Z"],["X","P"]]
         # ["G", "X", "Y", "S", "G", "Z", "S1", "N", "P", "Y1", "Z"], ["X", "P"]
   elif crystalStructure.lower() in ["orthorhombic", "orc", "op"]:
      # 6: ucv = pcv = [[1 0 0]', [0 2 0]', [0 0 3]']
      # symmetryKPoints = ["G","X","U","R","X","S","R","T","S","Y","T","Z","Y","G","Z","U","G"]
      symmetryKPoints = [["G","X","S","Y","G","Z","U","R","T","Z"],["Y","T"],["U","X"],["S","R"]]
      # ["G", "X", "S", "Y", "G", "Z", "U", "R", "T", "Z"], ["Y", "T"], ["U", "X"], ["S", "R"]
   elif crystalStructure.lower() in ["facecenteredorthorhombic", "orcf", "of"]:
      # 7: pcv = [[0 2/2 3/2]', [1./2., 0, 3/2]', [1./2. 2/2 0]']
      #    ucv = [[1 0 0]', [0 2 0]', [0 0 3]']
      pcv4fcc = np.array([[0, 1./2., 1./2.], [1./2., 0, 1./2.], [1./2., 1./2., 0]]).transpose()
      ucv4fcc = np.eye(3)
      pcv = avecStd
      ucv = pcv*(np.linalg.inv(pcv4fcc)*ucv4fcc)
      a = np.norm(ucv[:,0])
      b = np.norm(ucv[:,1])
      c = np.norm(ucv[:,2])
      d = (1./b**2 + 1./c**2 - 1./a**2) * max([a**2, b**2, c**2])
      if  d < -epsilon:
         type = "1"
      elif d > epsilon:
         type = "2"
      else:
         type = "3"
      if type is "1":
         # symmetryKPoints = [["G", "Y", "T", "Z", "G", "X", "A1", "Y"], ["T", "X1", "G", "L"], ["X", "A", "Z"]]
         symmetryKPoints = [["G","Y","T","Z","G","X","A1","Y"],["T","X1"],["X","A","Z"],["L","G"]]
         # ["G", "Y", "T", "Z", "G", "X", "A1", "Y"], ["T", "X1"], ["X", "A", "Z"], ["L", "G"]
      elif type is "2":
         # symmetryKPoints = [["G", "Y", "C", "D", "X", "G", "Z", "D1", "H", "C"], ["X", "H1", "G", "C1", "Z"], ["L", "G", "H", "Y"]]
         symmetryKPoints = [["G","Y","C","D","X","G","Z","D1","H","C"],["C1","Z"],["X","H1"],["H","Y"],["L","G"]]
         # ["G", "Y", "C", "D", "X", "G", "Z", "D1", "H", "C"], ["C1", "Z"], ["X", "H1"], ["H", "Y"], ["L", "G"]
      elif type is "3":
         # symmetryKPoints = [["L", "G", "Y", "T", "Z", "G", "X", "A1", "Y"], ["X", "A", "Z"]]
         symmetryKPoints = [["G","Y","T","Z","G","X","A1","Y"],["X","A","Z"],["L","G"]]
         # ["G", "Y", "T", "Z", "G", "X", "A1", "Y"], ["X", "A", "Z"], ["L", "G"]
   elif crystalStructure.lower() in ["bodycenteredorthorhombic", "orci", "oi"]:
      # 8: pcv = [[-1./2. 2/2 3/2]', [1./2., -2/2, 3/2]', [1./2. 2/2 -3/2]']
      #    ucv = [[1 0 0]', [0 2 0]', [0 0 3]']
      # symmetryKPoints = [["G", "X", "L", "T", "W", "R", "X1", "Z", "G", "Y", "S", "W"], ["Y", "L1", "G", "Y1", "Z"]]
      symmetryKPoints = [["G","X","L","T","W","R","X1","Z","G","Y","S","W"],["L1","Y"],["Y1","Z"]]
      # ["G", "X", "L", "T", "W", "R", "X1", "Z", "G", "Y", "S", "W"], ["L1", "Y"], ["Y1", "Z"]
   elif crystalStructure.lower() in ["ccenteredorthorhombic", "orcc", "os"]:
      # 9: pcv = [[1./2. -2/2 0]', [1./2., 2/2, 0]', [0 0 3]']
      #    ucv = [[1 0 0]', [0 2 0]', [0 0 3]']
      # symmetryKPoints = ["Z","T","G","X","S","R","A","Z","G","Y","X1","A1","T","Y"]
      symmetryKPoints = [["G","X","S","R","A","Z","G","Y","X1","A1","T","Y"],["Z","T"]]
      # ["G", "X", "S", "R", "A", "Z", "G", "Y", "X1", "A1", "T", "Y"], ["Z", "T"]
   elif crystalStructure.lower() in ["hexagonal", "hex", "hcp", "hp"]:
      # 10: ucv = pcv = [[1./2. -sqrt(3)/2 0]', [1./2., sqrt(3)/2, 0]', [0 0 3]']
      # symmetryKPoints = [["G", "M", "K", "G", "A", "L", "H", "A"], ["M", "L", "G", "K", "H"]]
      symmetryKPoints = [["G","M","K","G","A","L","H","A"],["L","M"],["K","H"]]
      # ["G", "M", "K", "G", "A", "L", "H", "A"], ["L", "M"], ["K", "H"]
   elif crystalStructure.lower() in ["rhombohedral", "rhl", "hr"]:
      # 11: ucv = pcv = [[cos(pi/5) -sin(pi/5) 0]', [cos(pi/5) sin(pi/5), 0]',
      #      [cos(2*pi/5)/cos(pi/5), 0, sqrt(1-(cos(2*pi/5)/cos(pi/5))**2)]']
      if np.dot(avecStd[:,2],avecStd[:,0]) > 0:
         type = "1"
      else:
         type = "2"
      if type is "1":
         # symmetryKPoints = [["L","P","G","L","B1","G","B","Z","G","X"],["Q","F","P1","Z"]]
         symmetryKPoints = [["G","L","B1"],["B","Z","G","X"],["Q","F","P1","Z"],["L","P"]]
         # ["G", "L", "B1"], ["B", "Z", "G", "X"], ["Q", "F", "P1", "Z"], ["L", "P"]
      elif type is "2":
         # symmetryKPoints = ["G", "P", "Z", "Q", "G", "F", "P1", "Q1", "L", "Z"]
         symmetryKPoints = [["G","P","Z","Q","G","F","P1","Q1","L","Z"]]
         # ["G", "P", "Z", "Q", "G", "F", "P1", "Q1", "L", "Z"]
   elif crystalStructure.lower() in ["monoclinic", "mcl", "mp"]:
      # 12: ucv = pcv = [[1 0 0]', [0 2 0]', [0, 3*cos(pi/5), 3*sin(pi/5)]']
      # symmetryKPoints = ["Y","D","G","Y","H","G","E","M1","A","X","H1","G","M","D","Z"]
      symmetryKPoints = [["G","Y","H","C","E","M1","A","X","G","Z","D","M"],["Z","A"],["D","Y"],["X","H1"]]
      # ["G", "Y", "H", "G", "E", "M1", "A", "X", "H1"], ["M", "D", "Z"], ["Y", "D"]
   elif crystalStructure.lower() in ["ccenteredmonoclinic", "mclc", "ms"]:
      # 13: pcv = [[1./2. 2/2 0]', [-1./2. 2/2 0]', [0, 3*cos(pi/5), 3*sin(pi/5)]']
      #     ucv = [[1 0 0]', [0 2 0]', [0, 3*cos(pi/5), 3*sin(pi/5)]']
      pcv = avecStd
      a = np.norm(pcv[:,0]-pcv[:,1])
      b = np.norm(pcv[:,0]+pcv[:,1])
      c = np.norm(pcv[:,2])
      kpcv = np.linalg.inv(pcv).transpose()
      kgamma = np.dot(kpcv[:,0],kpcv[:,1])/np.norm(kpcv[:,0])/np.norm(kpcv[:,1])
      if kgamma < -epsilon:
         type = "1"
      elif abs(kgamma) < epsilon:
         type = "2"
      else:
         cosalpha = np.dot(pcv[:,0]+pcv[:,1],pcv[:,2])/b/c
         sin2alpha = 1.-cosalpha**2
         d = b*cosalpha/c + (b**2*sin2alpha/a**2) - 1.
         if d < -epsilon:
            type = "3"
         elif abs(d) < epsilon:
            type = "4"
         else:
            type = "5"
      if type is "1":
         # symmetryKPoints = [["M","G","Y","F","L","I","G","I1","Z","F1","G","X1","Y"],["X", "G", "N"]]
         symmetryKPoints = [["G","Y","F","L","I"],["I1","Z","G","X"],["X1","Y"],["M","G","N"],["Z","F1"]]
         # ["G","Y", "F", "L", "I"], ["I1", "Z", "F1"], ["Y", "X1"], ["X", "G", "N"], ["M", "G"]
      elif type is "2":
         # symmetryKPoints = ["N","G","Y","F","L","I","G","I1","Z","F1","G","M"]
         symmetryKPoints = [["G","Y","F","L","I"],["I1","Z","F1"],["N","G","M"]]
         # ["G", "Y", "F", "L", "I"], ["I1", "Z", "F1"], ["N", "G", "M"]
      elif type is "3":
         # symmetryKPoints = ["M","G","Y","F","H","Z","I","F1","G","H1","Y1","X","G","N"]
         symmetryKPoints = [["G","Y","F","H","Z","I","X","G","Z"],["M","G","N"],["X","Y1","H1"],["I","F1"]]
         # ["G", "Y", "F", "H", "Z", "I", "F1"], ["H1", "Y1", "X", "G", "N"], ["M", "G"]
      elif type is "4":
         # symmetryKPoints = ["M","G","Y","F","H","Z","I","G","H1","Y1","X","G","N"]
         symmetryKPoints = [["G","Y","F","H","Z","I"],["H1","Y1","X","G","N"],["M","G"]]
         # ["G", "Y", "F", "H", "Z", "I"], ["H1", "Y1", "X", "G", "N"], ["M", "G"]
      elif type is "5":
         # symmetryKPoints = ["M","G","Y","F","L","I","G","I1","Z","H","F1","G","H1","Y1","X","G","N"]
         symmetryKPoints = [["G","Y","F","L","I"],["I1","Z","G","X","Y1","H1"],["H","F1"],["F2","X"],["M","G","N"],["H","Z"]]
         # ["G", "Y", "F", "L", "I"], ["I1", "Z", "H", "F1"], ["H1", "Y1", "X", "G", "N"], ["M", "G"]
   elif crystalStructure.lower() in ["triclinic", "tri", "ap"]:
      # 14: ucv = pcv = [[1 0 0]', [2*cos(pi/3), 2*sin(pi/3), 0]', [3*cos(pi/4),
      #      3/sin(pi/3)*(cos(pi/5)-cos(pi/4)*cos(pi/3)),
      #      3/sin(pi/3)*sqrt(1-(cos(pi/5))**2-(cos(pi/4))**2-(cos(pi/3))**2
      #      + 2*cos(pi/5)*cos(pi/4)*cos(pi/3))]'] : [1 2 3], [pi/5,pi/4,pi/3]
      kpcv = np.linalg.inv(avecStd).transpose()
      a = np.norm(kpcv[:,0])
      b = np.norm(kpcv[:,1])
      c = np.norm(kpcv[:,2])
      kalpha = np.dot(kpcv[:,1],kpcv[:,2])/b/c
      kbeta = np.dot(kpcv[:,2],kpcv[:,0])/c/a
      kgamma = np.dot(kpcv[:,0],kpcv[:,1])/a/b
      if kalpha < 0:
         if kgamma < -epsilon:
            type = "1a"
         else:
            type = "2a"
      else:
         if kgamma > epsilon:
            type = "1b"
         else:
            type = "2b"
      if type in ["1a","2a","1b","2b"]:
         symmetryKPoints = [["X", "G", "Y"], ["L", "G", "Z"], ["N", "G", "M"], ["R", "G"]]
         # ["X", "G", "Y"], ["L", "G", "Z"], ["N", "G", "M"], ["R", "G"]
   elif type is "0D":
      # 0D: isolate : [10 10 10]
      symmetryKPoints = ["G"]
   elif type is "1D":
      # 1D: along z direction. c << a,b : [10 10 1]
      symmetryKPoints = ["G", "X"]
   elif crystalStructure.lower() in ["square2d", "squ2d"]:
      # 2D1: along x-y plane. c >> a,b
      #     [[1 0 0]', [0, 1, 0]', [0 0 10]'] : [1 1 10]
      #     analog: Tetragonal
      symmetryKPoints = ["G", "X", "M", "G"]
   elif crystalStructure.lower() in ["rectangular2d", "rectangle2d", "rec2d"]:
      # 2D2: along x-y plane. c >> a,b
      #     [[1 0 0]', [0, 2, 0]', [0 0 10]'] : [1 1 10]
      #     analog: Orthorhombic
      symmetryKPoints = ["G", "X", "S", "Y", "G", "S"]
   elif crystalStructure.lower() in ["hexagonal2d", "hexagon2d", "hex2d"]:
      # 2D3: along x-y plane. c >> a,b
      #     [[1./2. -sqrt(3)/2 0]', [1./2., sqrt(3)/2, 0]', [0 0 10]'] : [1 1 10]
      #     analog: Hexagonal
      symmetryKPoints = ["G", "M", "K", "G"]
   elif crystalStructure.lower() in ["rhombic2d", "rhombus2d", "centeredrectangular2d", "rho2d"]:
      # 2D4:  along x-y plane. c >> a,b
      #     [[1./2. -2/2 0]', [1./2., 2/2, 0]', [0 0 10]'] : [1 2 10]
      #     analog: CCenteredOrthorhombic
      #     pcv = [[1./2. -2/2 0]', [1./2., 2/2, 0]', [0 0 10]']
      #     ucv = [[1 0 0]', [0 2 0]', [0 0 10]']
      symmetryKPoints = ["S","G","X","S","X1","Y","G","X1"]
   elif crystalStructure.lower() in ["oblique2d", "obl2d"]:
      # 2D5:  along x-y plane. c >> a,b
      #     [[2 0 0]', [3*cos(pi/5), 3*sin(pi/5), 0]', [0 0 10]'] : [2 3 10]
      #     analog: "Monoclinic"
      symmetryKPoints = ["H","G","Y","H","C","G","X","H1","G","Y1","H2"]
   else:
      raise NameError("Crystal structure not recognized.")
   return symmetryKPoints

def kValue2kSymbol(crystalStructure, primitiveCellVectors, kValue):
   """
   This function finds a high-symmetry k-point label from reduced coordinates.

   Parameters
   ----------
   crystalStructure : string
      Name of the Bravais lattice.

   primitiveCellVectors : 2D array
      3 x 3 array of row-vectors corresponding to the lattice vectors).

   kValue : 1D array
      High-symmetry k-point fractional coordinates.

   Returns
   -------
   kSymbol: string
      High-symmetry k-point label.

   Author Info:
   Vincent Michaud-Rioux
   2020-06-23
   """
   if isinstance(kValue, list):
      return [kValue2kSymbol(crystalStructure, primitiveCellVectors, k) for k in kValue]

   if isinstance(kValue, str):
      return kValue

   kptDict = kSymbol_2_kValue_dict(crystalStructure, primitiveCellVectors)
   kSymbol = "!"
   for i in kptDict.keys():
      if np.allclose(kValue, kptDict[i], rtol=1.e-5, atol=1.e-5):
         kSymbol = i
         break
   return kSymbol

def kSymbol2kValue(crystalStructure, primitiveCellVectors, kSymbol):
   """
   This function is to convert a high-symmetry k-point label to reduced coordinates.

   This function is to convert a conventional symbol for a high
   symmetrical point in k space into its corresponding coordinate
   value, where the unit of the value is the three reciprocal primitive
   cell vectors.
   Please note that each symbol actually represents a set of infinitely 
   many equivalent points and the output coordinates is just for one of them.

   Parameters
   ----------
   crystalStructure : string
      Name of the Bravais lattice.

   primitiveCellVectors : 2D array
      3 x 3 array of row-vectors corresponding to the lattice vectors).

   kSymbol: string
      High-symmetry k-point label.

   Returns
   -------
   kValue : 1D array
      High-symmetry k-point fractional coordinates.

   Author Info:
   Vincent Michaud-Rioux
   2020-06-23
   """
   if isinstance(kSymbol, list):
      return [kSymbol2kValue(crystalStructure, primitiveCellVectors, k) for k in kSymbol]

   if not isinstance(kSymbol, str):
      return np.array(kSymbol)

   kptDict = kSymbol_2_kValue_dict(crystalStructure, primitiveCellVectors)
   if not kSymbol in kptDict.keys():
      NameError("Unknown symbol "+kSymbol+" for Bravais lattice "+crystalStructure+".")        
   return np.array(kptDict[kSymbol])

def kSymbol_2_kValue_dict(crystalStructure, primitiveCellVectors):
   """
   This function returns a dictionary of the high-symmetry k-point labels
   of a given crystal structure in reduced coordinates.

   Parameters
   ----------
   crystalStructure : string
      Name of the Bravais lattice.

   primitiveCellVectors : 2D array
      3 x 3 array of row-vectors corresponding to the lattice vectors).

   Returns
   -------
   kptDict : dict
      High-symmetry k-points in fractional coordinates.

   Author Info:
   Lei Liu, HZWTech
   2015-10
   Vincent Michaud-Rioux
   2020-06-23

   ############## about the symbol of the symmetry k points ##################
   ## This is simply the convention for labeling points of high symmetry in
   ## the Brillouin zone.  It"s origin is: Bouckaert, Smoluchowski, and
   ## Wigner, "Theory of Brillouin Zones and Symmetry Properties of Wave
   ## Functions in Crystals," Phys. Rev. 50, p. 58 (1936).  The guide to all
   ## the details of this is John C. Slater, "Symmetry and Energy Bands in
   ## Crystals" (reprinted by Dover in 1972).  It has all the 3-d crystal
   ## structures and, I suspect, 2-d as well.  These labels may make some
   ## sense in the context of group theory (or perhaps in Hungarian), but
   ## they are commonly regarded as an arbitrary but common convention.
   ##
   ## It is also called critical point. see http://en.wikipedia.org/wiki/Brillouin_zone
   ###########################################################################
   """

   primitiveCellVectors = primitiveCellVectors.transpose() # here primitiveCellVectors = [a1 a2 a3]
   kptDict = {}
   epsilon = 1e-3
   if crystalStructure.lower() in ["cubic","cub","simplecubic","sc","cp"]:
      # 1: ucv = pcv = [[1 0., 0]',[0., 1 0]',[0., 0., 1]']
      kSymbols = ["G","X","M","R"]
      kptDict[kSymbols[0]] = [0., 0., 0.] # Gamma: Center of the Brillouin zone
      kptDict[kSymbols[1]] = [0., .5, 0.] # X: Center of a face
      kptDict[kSymbols[2]] = [.5, .5, 0.] # M: Center of an edge
      kptDict[kSymbols[3]] = [.5, .5, .5] # R: Corner point
   elif crystalStructure.lower() in ["facecenteredcubic","fcc","cf"]:
      # 2: pcv = [[0., .5, .5]',[.5,0,.5]',[.5, .5, 0]']
      #    ucv = [[1 0., 0]',[0., 1 0]',[0., 0., 1]']
      kSymbols = ["G","K","L","U","W","X"]
      kptDict[kSymbols[0]] = [0., 0., 0]  # Gamma: Center of the Brillouin zone
      kptDict[kSymbols[1]] = [3/8, 3/8, 3/4] # K: Middle of an edge joining two hexagonal faces
      kptDict[kSymbols[2]] = [.5, .5, .5] # L: Center of a hexagonal face
      kptDict[kSymbols[3]] = [5/8, 1/4, 5/8] # U: Middle of an edge joining a hexagonal and a square face
      kptDict[kSymbols[4]] = [.5, 1/4, 3/4]  # W : Corner point
      kptDict[kSymbols[5]] = [.5, 0., .5]  # X: Center of a square face
   elif crystalStructure.lower() in ["bodycenteredcubic","bcc","ci"]:
      # 3: pcv = [[-.5, .5, .5]',[.5,-.5,.5]',[.5, .5, -.5]']
      #    ucv = [[1 0., 0]',[0., 1 0]',[0., 0., 1]']
      kSymbols = ["G","H","P","N"]
      kptDict[kSymbols[0]] = [0., 0., 0]  # Gamma: Center of the Brillouin zone
      kptDict[kSymbols[1]] = [.5, -.5, .5] # H: Corner point joining four edges
      kptDict[kSymbols[2]] = [1/4, 1/4, 1/4] # P: Corner point joining three edges
      kptDict[kSymbols[3]] = [0., 0., .5] # N: Center of a face
   elif crystalStructure.lower() in ["tetragonal","tet","tp"]:
      # 4: ucv = pcv = [[1 0., 0]',[0., 1 0]',[0., 0., 5]']
      kSymbols = ["G","A","M","R","X","Z"]
      kptDict[kSymbols[0]] = [0., 0., 0]  # Gamma: Center of the Brillouin zone
      kptDict[kSymbols[1]] = [.5, .5, .5]
      kptDict[kSymbols[2]] = [.5, .5, 0]
      kptDict[kSymbols[3]] = [0., .5, .5]
      kptDict[kSymbols[4]] = [0., .5, 0]
      kptDict[kSymbols[5]] = [0., 0., .5]
   elif crystalStructure.lower() in ["bodycenteredtetragonal","bct","ti"]:
      # 5: pcv = [[-.5, .5, 5/2]',[.5,-.5,5/2]',[.5, .5, -5/2]']
      #    ucv = [[1 0., 0]',[0., 1 0]',[0., 0., 5]']
      pcv4bcc = np.array([[-.5, .5, .5],[.5,-.5,.5],[.5, .5, -.5]]).transpose()
      ucv4bcc = np.eye(3)
      pcv = primitiveCellVectors
      ucv = np.matmul(pcv, np.linalg.solve(pcv4bcc,ucv4bcc))
      if np.linalg.norm(ucv[:,2]) < np.linalg.norm(ucv[:,0]):
         type = "1"
      else:
         type = "2"
      if type == "1":
         a = np.linalg.norm(ucv[:,0])
         c = np.linalg.norm(ucv[:,2])
         eta = (1 + c**2/a**2)/4
         kSymbols = ["G","M","N","P","X","Z","Z1"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [-.5, .5, .5]
         kptDict[kSymbols[2]] = [0., .5, 0]
         kptDict[kSymbols[3]] = [1/4, 1/4, 1/4]
         kptDict[kSymbols[4]] = [0., 0., .5]
         kptDict[kSymbols[5]] = [eta, eta, -eta]
         kptDict[kSymbols[6]] = [-eta, 1-eta, eta]
      elif type == "2":
         a = np.linalg.norm(ucv[:,0])
         c = np.linalg.norm(ucv[:,2])
         eta = (1. + a**2/c**2)/4.
         zeta = a**2/c**2/2.
         kSymbols = ["G","N","P","X","Z","S","S1","Y","Y1"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [0., .5, 0]
         kptDict[kSymbols[2]] = [1/4, 1/4, 1/4]
         kptDict[kSymbols[3]] = [0., 0., .5]
         kptDict[kSymbols[4]] = [.5, .5, -.5]
         kptDict[kSymbols[5]] = [-eta, eta, eta]
         kptDict[kSymbols[6]] = [eta, 1-eta, -eta]
         kptDict[kSymbols[7]] = [-zeta, zeta, .5]
         kptDict[kSymbols[8]] = [.5, .5, -zeta]
   elif crystalStructure.lower() in ["orthorhombic","orc","op"]:
      # 6: ucv = pcv = [[1 0., 0]',[0., 2 0]',[0., 0., 3]']
      kSymbols = ["G","R","S","T","U","X","Y","Z"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [.5, .5, .5]
      kptDict[kSymbols[2]] = [.5, .5, 0]
      kptDict[kSymbols[3]] = [0., .5, .5]
      kptDict[kSymbols[4]] = [.5, 0., .5]
      kptDict[kSymbols[5]] = [.5, 0., 0]
      kptDict[kSymbols[6]] = [0., .5, 0]
      kptDict[kSymbols[7]] = [0., 0., .5]
   elif crystalStructure.lower() in ["facecenteredorthorhombic","orcf","of"]:
      # 7: pcv = [[0., 2/2 3/2]',[.5,0,3/2]',[.5, 2/2 0]']
      #    ucv = [[1 0., 0]',[0., 2 0]',[0., 0., 3]']
      pcv4fcc = np.array([[0., .5, .5],[.5,0,.5],[.5, .5, 0]]).transpose()
      ucv4fcc = np.eye(3)
      pcv = primitiveCellVectors
      ucv = np.matmul(pcv, np.linalg.solve(pcv4fcc, ucv4fcc))
      a = np.linalg.norm(ucv[:,0])
      b = np.linalg.norm(ucv[:,1])
      c = np.linalg.norm(ucv[:,2])
      d = (1/b**2 + 1/c**2 - 1/a**2) * max([a**2,b**2,c**2])
      if  d < -epsilon:
         type = "1"
      elif d > epsilon:
         type = "2"
      else:
         type = "3"
      if type in ["1", "3"]:
         eta = (1. + a**2/b**2 + a**2/c**2)/4.
         zeta = (1. + a**2/b**2 - a**2/c**2)/4.
         kSymbols = ["G","L","T","Y","Z","A","A1","X","X1"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, .5, .5]
         kptDict[kSymbols[2]] = [1, .5, .5]
         kptDict[kSymbols[3]] = [.5, 0., .5]
         kptDict[kSymbols[4]] = [.5, .5, 0]
         kptDict[kSymbols[5]] = [.5, .5+zeta, zeta]
         kptDict[kSymbols[6]] = [.5, .5-zeta, 1-zeta]
         kptDict[kSymbols[7]] = [0., eta, eta]
         kptDict[kSymbols[8]] = [1, 1-eta, 1-eta]
      elif type == "2":
         eta = (1 + a**2/b**2 - a**2/c**2)/4
         delta = (1 + b**2/a**2 - b**2/c**2)/4
         phi = (1 + c**2/b**2 - c**2/a**2)/4
         kSymbols = ["G","L","X","Y","Z","C","C1","D","D1","H","H1"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, .5, .5]
         kptDict[kSymbols[2]] = [0., .5, .5]
         kptDict[kSymbols[3]] = [.5, 0., .5]
         kptDict[kSymbols[4]] = [.5, .5, 0]
         kptDict[kSymbols[5]] = [.5, .5-eta, 1-eta]
         kptDict[kSymbols[6]] = [.5, .5+eta, eta]
         kptDict[kSymbols[7]] = [.5-delta, .5, 1-delta]
         kptDict[kSymbols[8]] = [.5+delta, .5, delta]
         kptDict[kSymbols[9]] = [1-phi, .5-phi, .5]
         kptDict[kSymbols[10]] = [phi, .5+phi, .5]
   elif crystalStructure.lower() in ["bodycenteredorthorhombic","orci","oi"]:
      # 8: pcv = [[-.5, 2/2 3/2]',[.5,-2/2,3/2]',[.5, 2/2 -3/2]']
      #    ucv = [[1 0., 0]',[0., 2 0]',[0., 0., 3]']
      pcv4bcc = np.array([[-.5, .5, .5],[.5,-.5,.5],[.5, .5, -.5]]).transpose()
      ucv4bcc = np.eye(3)
      pcv = primitiveCellVectors
      ucv = np.matmul(pcv, np.linalg.solve(pcv4bcc, ucv4bcc))
      a = np.linalg.norm(ucv[:,0])
      b = np.linalg.norm(ucv[:,1])
      c = np.linalg.norm(ucv[:,2])
      zeta = (1 + a**2/c**2)/4
      eta = (1 + b**2/c**2)/4
      delta = (b**2 - a**2)/(4*c**2)
      mu = (a**2 + b**2)/(4*c**2)
      kSymbols = ["G","R","S","T","W","Z","L","L1","L2","X","X1","Y","Y1"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., .5, 0]
      kptDict[kSymbols[2]] = [.5, 0., 0]
      kptDict[kSymbols[3]] = [0., 0., .5]
      kptDict[kSymbols[4]] = [1/4, 1/4, 1/4]
      kptDict[kSymbols[5]] = [.5, .5, -.5]
      kptDict[kSymbols[6]] = [-mu, mu, .5-delta]
      kptDict[kSymbols[7]] = [mu, -mu, .5+delta]
      kptDict[kSymbols[8]] = [.5-delta, .5+delta, -mu]
      kptDict[kSymbols[9]] = [-zeta, zeta, zeta]
      kptDict[kSymbols[10]] = [zeta, 1-zeta, -zeta]
      kptDict[kSymbols[11]] = [eta, -eta, eta]
      kptDict[kSymbols[12]] = [1-eta, eta, -eta]
   elif crystalStructure.lower() in ["ccenteredorthorhombic","orcc","os"]:
      # 9: pcv = [[.5, -2/2 0]',[.5,2/2,0]',[0., 0., 3]']
      #    ucv = [[1 0., 0]',[0., 2 0]',[0., 0., 3]']
      pcv = primitiveCellVectors
      a = np.linalg.norm(pcv[:,0]+pcv[:,1])
      b = np.linalg.norm(pcv[:,0]-pcv[:,1])
      zeta = (1 + a**2/b**2)/4
      kSymbols = ["G","R","S","T","Y","Z","A","A1","X","X1"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., .5, .5]
      kptDict[kSymbols[2]] = [0., .5, 0]
      kptDict[kSymbols[3]] = [-.5, .5, .5]
      kptDict[kSymbols[4]] = [-.5, .5, 0]
      kptDict[kSymbols[5]] = [0., 0., .5]
      kptDict[kSymbols[6]] = [zeta, zeta, .5]
      kptDict[kSymbols[7]] = [-zeta, 1-zeta, .5]
      kptDict[kSymbols[8]] = [zeta, zeta, 0]
      kptDict[kSymbols[9]] = [-zeta, 1-zeta, 0]
   elif crystalStructure.lower() in ["hexagonal","hex","hcp","hp"]:
      # 10: ucv = pcv = [[.5, -sqrt(3)/2 0]',[.5,sqrt(3)/2,0]',[0., 0., 3]']
      kSymbols = ["G","A","H","K","L","M"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., 0., .5]
      kptDict[kSymbols[2]] = [1/3, 1/3, .5]
      kptDict[kSymbols[3]] = [1/3, 1/3, 0]
      kptDict[kSymbols[4]] = [.5, 0., .5]
      kptDict[kSymbols[5]] = [.5, 0., 0]
   elif crystalStructure.lower() in ["rhombohedral","rhl","hr"]:
      # 11: ucv = pcv = [[cos(pi/5) -sin(pi/5) 0]',[cos(pi/5) sin(pi/5),0]',
      #      [cos(2*pi/5)/cos(pi/5),0,sqrt(1-(cos(2*pi/5)/cos(pi/5))**2)]']
      pcv = primitiveCellVectors
      cosalpha = np.dot(pcv[:,2],pcv[:,0])/np.linalg.norm(pcv[:,0])/np.linalg.norm(pcv[:,2])
      if cosalpha > 0:
         type = "1"
      else:
         type = "2"
      if type == "1":
         eta = (1 + 4*cosalpha)/(2 + 4*cosalpha)
         nu = 3/4 - eta/2
         kSymbols = ["G","F","L","L1","Z","B","B1","P","P1","P2","Q","X"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, .5, 0]
         kptDict[kSymbols[2]] = [.5, 0., 0]
         kptDict[kSymbols[3]] = [0., 0., -.5]
         kptDict[kSymbols[4]] = [.5, .5, .5]
         kptDict[kSymbols[5]] = [eta, .5, 1-eta]
         kptDict[kSymbols[6]] = [.5, 1-eta, eta-1]
         kptDict[kSymbols[7]] = [eta, nu, nu]
         kptDict[kSymbols[8]] = [1-nu, 1-nu, 1-eta]
         kptDict[kSymbols[9]] = [nu, nu, eta-1]
         kptDict[kSymbols[10]] = [1-nu, nu, 0]
         kptDict[kSymbols[11]] = [nu, 0., -nu]
      elif type == "2":
         eta = (.5)*(1+cosalpha)/(1-cosalpha)
         nu = 3/4 - eta/2
         kSymbols = ["G","F","L","Z","P","P1","Q","Q1"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, -.5, 0]
         kptDict[kSymbols[2]] = [.5, 0., 0]
         kptDict[kSymbols[3]] = [.5, -.5, .5]
         kptDict[kSymbols[4]] = [1-nu, -nu, 1-nu]
         kptDict[kSymbols[5]] = [nu, nu-1, nu-1]
         kptDict[kSymbols[6]] = [eta, eta, eta]
         kptDict[kSymbols[7]] = [1-eta, -eta, -eta]
   elif crystalStructure.lower() in ["monoclinic","mcl","mp"]:
      # 12: ucv = pcv = [[1 0., 0]',[0., 2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      pcv = primitiveCellVectors
      b = np.linalg.norm(pcv[:,1])
      c = np.linalg.norm(pcv[:,2])
      cosalpha = np.dot(pcv[:,1],pcv[:,2])/b/c
      sin2alpha = 1-cosalpha**2
      eta = (1 - b*cosalpha/c)/(2*sin2alpha)
      nu = .5 - eta*c*cosalpha/b
      kSymbols = ["G","A","C","D","D1","E","X","Y","Y1","Z","H","H1","H2","M","M1","M2"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [.5, .5, 0]
      kptDict[kSymbols[2]] = [0., .5, .5]
      kptDict[kSymbols[3]] = [.5, 0., .5]
      kptDict[kSymbols[4]] = [.5, 0., -.5]
      kptDict[kSymbols[5]] = [.5, .5, .5]
      kptDict[kSymbols[6]] = [0., .5, 0]
      kptDict[kSymbols[7]] = [0., 0., .5]
      kptDict[kSymbols[8]] = [0., 0., -.5]
      kptDict[kSymbols[9]] = [.5, 0., 0]
      kptDict[kSymbols[10]] = [0., eta, 1-nu]
      kptDict[kSymbols[11]] = [0., 1-eta, nu]
      kptDict[kSymbols[12]] = [0., eta, -nu]
      kptDict[kSymbols[13]] = [.5, eta, 1-nu]
      kptDict[kSymbols[14]] = [.5, 1-eta, nu]
      kptDict[kSymbols[15]] = [.5, eta, -nu]
   elif crystalStructure.lower() in ["ccenteredmonoclinic","mclc","ms"]:
      # 13: pcv = [[.5, 2/2 0]',[-.5, 2/2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      #     ucv = [[1 0., 0]',[0., 2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      pcv = primitiveCellVectors
      a = np.linalg.norm(pcv[:,0]-pcv[:,1])
      b = np.linalg.norm(pcv[:,0]+pcv[:,1])
      c = np.linalg.norm(pcv[:,2])
      kpcv = np.linalg.inv(pcv).transpose()
      kgamma = np.dot(kpcv[:,0],kpcv[:,1])/np.linalg.norm(kpcv[:,0])/np.linalg.norm(kpcv[:,1])
      if kgamma < -epsilon:
         type = "1"
      elif abs(kgamma) < epsilon:
         type = "2"
      else:
         cosalpha = np.dot(pcv[:,0]+pcv[:,1],pcv[:,2])/b/c
         sin2alpha = 1-cosalpha**2
         d = b*cosalpha/c + b**2*sin2alpha/a**2 - 1
         if d < -epsilon:
            type = "3"
         elif abs(d) < epsilon:
            type = "4"
         else:
            type = "5"
      if type in ["1", "2"]:
         cosalpha = np.dot(pcv[:,0]+pcv[:,1],pcv[:,2])/b/c
         sin2alpha = 1-cosalpha**2
         zeta = (2-b*cosalpha/c)/(4*sin2alpha)
         eta = .5 + 2*zeta*c*cosalpha/b
         psi = 3/4 - a**2/(4*b**2*sin2alpha)
         phi = psi + (3/4-psi)*b*cosalpha/c
         kSymbols = ["G","N","N1","L","M","Y","Y1","Z","F","F1","F2","F3","I","I1","X","X1","X2"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, 0., 0]
         kptDict[kSymbols[2]] = [0., -.5, 0]
         kptDict[kSymbols[3]] = [.5, .5, .5]
         kptDict[kSymbols[4]] = [.5, 0., .5]
         kptDict[kSymbols[5]] = [.5, .5, 0]
         kptDict[kSymbols[6]] = [-.5, -.5, 0]
         kptDict[kSymbols[7]] = [0., 0., .5]
         kptDict[kSymbols[8]] = [1-zeta, 1-zeta, 1-eta]
         kptDict[kSymbols[9]] = [zeta, zeta, eta]
         kptDict[kSymbols[10]] = [-zeta, -zeta, 1-eta]
         kptDict[kSymbols[11]] = [1-zeta, -zeta, 1-eta]
         kptDict[kSymbols[12]] = [phi, 1-phi, .5]
         kptDict[kSymbols[13]] = [1-phi, phi-1, .5]
         kptDict[kSymbols[14]] = [1-psi, psi-1, 0]
         kptDict[kSymbols[15]] = [psi, 1-psi, 0]
         kptDict[kSymbols[16]] = [psi-1, -psi, 0]
      elif type in ["3", "4"]:
         cosalpha = np.dot(pcv[:,0]+pcv[:,1],pcv[:,2])/b/c
         sin2alpha = 1-cosalpha**2
         mu = (1 + b**2/a**2)/4
         delta = b*c*cosalpha/(2*a**2)
         zeta = mu - 1/4 + (1-b*cosalpha/c)/(4*sin2alpha)
         eta = .5 + 2*zeta*c*cosalpha/b
         phi = 1 + zeta - 2*mu
         psi = eta - 2*delta
         kSymbols = ["G","I","M","N","N1","X","Z","F","F1","F2","H","H1","H2","Y","Y1","Y2","Y3"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, -.5, .5]
         kptDict[kSymbols[2]] = [.5, 0., .5]
         kptDict[kSymbols[3]] = [.5, 0., 0]
         kptDict[kSymbols[4]] = [0., -.5, 0]
         kptDict[kSymbols[5]] = [.5, -.5, 0]
         kptDict[kSymbols[6]] = [0., 0., .5]
         kptDict[kSymbols[7]] = [1-phi, 1-phi, 1-psi]
         kptDict[kSymbols[8]] = [phi, phi-1, psi]
         kptDict[kSymbols[9]] = [1-phi, -phi, 1-psi]
         kptDict[kSymbols[10]] = [zeta, zeta, eta]
         kptDict[kSymbols[11]] = [1-zeta, -zeta, 1-eta]
         kptDict[kSymbols[12]] = [-zeta, -zeta, 1-eta]
         kptDict[kSymbols[13]] = [mu, mu, delta]
         kptDict[kSymbols[14]] = [1-mu, -mu, -delta]
         kptDict[kSymbols[15]] = [-mu, -mu, -delta]
         kptDict[kSymbols[16]] = [mu, mu-1, delta]
      elif type == "5":
         cosalpha = np.dot(pcv[:,0]+pcv[:,1],pcv[:,2])/b/c
         sin2alpha = 1-cosalpha**2
         zeta = (b**2/a**2 + (1 - b*cosalpha/c)/sin2alpha)/4
         eta = .5 + 2*zeta*c*cosalpha/b
         mu = eta/2 + b**2/(4*a**2) - b*c*cosalpha/(2*a**2)
         nu = 2*mu - zeta
         omega = (4*nu - 1 - b**2*sin2alpha/a**2)*c/(2*b*cosalpha)
         delta = zeta*c*cosalpha/b + omega/2 - 1/4
         rho = 1 - zeta*a**2/b**2
         kSymbols = ["G","L","M","N","N1","X","Z","F","F1","F2","H","H1","H2","I","I1","Y","Y1","Y2","Y3"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, .5, .5]
         kptDict[kSymbols[2]] = [.5, 0., .5]
         kptDict[kSymbols[3]] = [.5, 0., 0]
         kptDict[kSymbols[4]] = [0., -.5, 0]
         kptDict[kSymbols[5]] = [.5, -.5, 0]
         kptDict[kSymbols[6]] = [0., 0., .5]
         kptDict[kSymbols[7]] = [nu, nu, omega]
         kptDict[kSymbols[8]] = [1-nu, 1-nu, 1-omega]
         kptDict[kSymbols[9]] = [nu, nu-1, omega]
         kptDict[kSymbols[10]] = [zeta, zeta, eta]
         kptDict[kSymbols[11]] = [1-zeta, -zeta, 1-eta]
         kptDict[kSymbols[12]] = [-zeta, -zeta, 1-eta]
         kptDict[kSymbols[13]] = [rho, 1-rho, .5]
         kptDict[kSymbols[14]] = [1-rho, rho-1, .5]
         kptDict[kSymbols[15]] = [mu, mu, delta]
         kptDict[kSymbols[16]] = [1-mu, -mu, -delta]
         kptDict[kSymbols[17]] = [-mu, -mu, -delta]
         kptDict[kSymbols[18]] = [mu, mu-1, delta]
   elif crystalStructure.lower() in ["triclinic","tri","ap"]:
      # 14: ucv = pcv = [[1 0., 0]',[2*cos(pi/3),2*sin(pi/3),0]',[3*cos(pi/4),
      #      3/sin(pi/3)*(cos(pi/5)-cos(pi/4)*cos(pi/3)),
      #      3/sin(pi/3)*sqrt(1-(cos(pi/5))**2-(cos(pi/4))**2-(cos(pi/3))**2
      #      + 2*cos(pi/5)*cos(pi/4)*cos(pi/3))]'] :: [1 2 3],[pi/5,pi/4,pi/3]
      kpcv = np.linalg.inv(primitiveCellVectors).transpose()
      a = np.linalg.norm(kpcv[:,0])
      b = np.linalg.norm(kpcv[:,1])
      c = np.linalg.norm(kpcv[:,2])
      kalpha = np.dot(kpcv[:,1],kpcv[:,2])/b/c
      # kbeta = np.dot(kpcv[:,2],kpcv[:,0])/c/a
      kgamma = np.dot(kpcv[:,0],kpcv[:,1])/a/b
      if kalpha < 0:
         if kgamma < -epsilon:
            type = "1a"
         else:
            type = "2a"
      else:
         if kgamma > epsilon:
            type = "1b"
         else:
            type = "2b"
      if type in ["1a","2a"]:
         kSymbols = ["G","L","M","N","R","X","Y","Z"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, .5, 0]
         kptDict[kSymbols[2]] = [0., .5, .5]
         kptDict[kSymbols[3]] = [.5, 0., .5]
         kptDict[kSymbols[4]] = [.5, .5, .5]
         kptDict[kSymbols[5]] = [.5, 0., 0]
         kptDict[kSymbols[6]] = [0., .5, 0]
         kptDict[kSymbols[7]] = [0., 0., .5]
      elif type in ["1b","2b"]:
         kSymbols = ["G","L","M","N","R","X","Y","Z"]
         kptDict[kSymbols[0]] = [0., 0., 0]
         kptDict[kSymbols[1]] = [.5, -.5, 0]
         kptDict[kSymbols[2]] = [0., 0., .5]
         kptDict[kSymbols[3]] = [-.5, -.5, .5]
         kptDict[kSymbols[4]] = [0., -.5, .5]
         kptDict[kSymbols[5]] = [0., -.5, 0]
         kptDict[kSymbols[6]] = [.5, 0., 0]
         kptDict[kSymbols[7]] = [-.5, 0., .5]
   elif crystalStructure == "0D":
      # 0D: isolate :: [10., 10., 10]
      kSymbols = ["G"]
      kptDict[kSymbols[0]] = [0., 0., 0]
   elif crystalStructure == "1D":
      # 1D: along z direction. c << a,b :: [10., 10., 1]
      kSymbols = ["G","X"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., 0., .5]
   elif crystalStructure.lower() in ["square2d","squ2d"]:
      # 2D1: along x-y plane. c >> a,b
      #     [[1 0., 0]',[0,1,0]',[0., 0., 10]'] :: [1 1 10]
      #     analog: Tetragonal
      kSymbols = ["G","X","M"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., .5, 0]
      kptDict[kSymbols[2]] = [.5, .5, 0]
   elif crystalStructure.lower() in ["rectangular2d","rectangle2d","rec2d"]:
      # 2D2: along x-y plane. c >> a,b
      #     [[1 0., 0]',[0,2,0]',[0., 0., 10]'] :: [1 1 10]
      #     analog: Orthorhombic
      kSymbols = ["G","X","Y","S"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [.5, 0., 0]
      kptDict[kSymbols[2]] = [0., .5, 0]
      kptDict[kSymbols[3]] = [.5, .5, 0]
   elif crystalStructure.lower() in ["hexagonal2d","hexagon2d","hex2d"]:
      # 2D3: along x-y plane. c >> a,b
      #     [[.5, -sqrt(3)/2 0]',[.5,sqrt(3)/2,0]',[0., 0., 10]'] :: [1 1 10]
      #     analog: Hexagonal
      kSymbols = ["G","M","K"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [.5, 0., 0]
      kptDict[kSymbols[2]] = [1/3, 1/3, 0]
   elif crystalStructure.lower() in ["rhombic2d","rhombus2d","centeredrectangular2d","rho2d"]:
      # 2D4:  along x-y plane. c >> a,b
      #     [[.5, -2/2 0]',[.5,2/2,0]',[0., 0., 10]'] :: [1 2 10]
      #     analog: CCenteredOrthorhombic
      #     pcv = [[.5, -2/2 0]',[.5,2/2,0]',[0., 0., 10]']
      #     ucv = [[1 0., 0]',[0., 2 0]',[0., 0., 10]']
      pcv = primitiveCellVectors
      a = np.linalg.norm(pcv[:,0]+pcv[:,1])
      b = np.linalg.norm(pcv[:,0]-pcv[:,1])
      zeta = (1 + a**2/b**2)/4
      kSymbols = ["G","S","Y","X","X1"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [0., .5, 0]
      kptDict[kSymbols[2]] = [-.5, .5, 0]
      kptDict[kSymbols[3]] = [zeta, zeta, 0]
      kptDict[kSymbols[4]] = [-zeta, 1-zeta, 0]
   elif crystalStructure.lower() in ["oblique2d","obl2d"]:
      # 2D5:  along x-y plane. c >> a,b
      #     [[2 0., 0]',[3*cos(pi/5),3*sin(pi/5),0]',[0., 0., 10]'] :: [2 3 10]
      #     analog: "Monoclinic"
      pcv = primitiveCellVectors
      b = np.linalg.norm(pcv[:,0])
      c = np.linalg.norm(pcv[:,1])
      cosalpha = np.dot(pcv[:,0],pcv[:,1])/b/c
      sin2alpha = 1-cosalpha**2
      eta = (1 - b*cosalpha/c)/(2*sin2alpha)
      nu = .5 - eta*c*cosalpha/b
      kSymbols = ["G","C","X","Y","Y1","H","H1","H2"]
      kptDict[kSymbols[0]] = [0., 0., 0]
      kptDict[kSymbols[1]] = [.5, .5, 0]
      kptDict[kSymbols[2]] = [.5, 0., 0]
      kptDict[kSymbols[3]] = [0., .5, 0]
      kptDict[kSymbols[4]] = [0., -.5, 0]
      kptDict[kSymbols[5]] = [eta, 1-nu, 0]
      kptDict[kSymbols[6]] = [1-eta, nu, 0]
      kptDict[kSymbols[7]] = [eta, -nu, 0]
   else:
      NameError("Unknown crystal structure "+crystalStructure+".")
   return kptDict

###########
# testing #
###########

def print_kvalues(crystalStructure, avec, kSymbols):
   for i in range(0, len(kSymbols)):
      kval = kSymbol2kValue(crystalStructure, avec, kSymbols[i])
      print('%6s %6s %f %f %f' % (crystalStructure, kSymbols[i], kval[0], kval[1], kval[2]))

def print_all_bra2avec():
   perm = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]

   crystalStructure = 'CUB'; avec = bra2avec('CUB')
   kSymbols = ['G','X','M','R']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'CUB')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'FCC'; avec = bra2avec('FCC')
   kSymbols = ['G','K','L','U','W','X']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'FCC')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'BCC'; avec = bra2avec('BCC')
   kSymbols = ['G','H','P','N']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'BCC')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'TET'; avec = bra2avec('TET1')
   kSymbols = ['G','A','M','R','X','Z']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'TET1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'TET'; avec = bra2avec('TET2')
   kSymbols = ['G','A','M','R','X','Z']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'TET2')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'BCT'; avec = bra2avec('BCT1')
   kSymbols = ['G','M','N','P','X','Z','Z1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'BCT1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'BCT'; avec = bra2avec('BCT2')
   kSymbols = ['G','N','P','X','Z','S','S1','Y','Y1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'BCT2')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORC'; avec = bra2avec('ORC')
   kSymbols = ['G','R','S','T','U','X','Y','Z']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORC')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF1')
   kSymbols = ['G','L','T','Y','Z','A','A1','X','X1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORCF1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF2')
   kSymbols = ['G','L','X','Y','Z','C','C1','D','D1','H','H1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORCF2')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF3')
   kSymbols = ['G','L','T','Y','Z','A','A1','X','X1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORCF3')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORCI'; avec = bra2avec('ORCI')
   kSymbols = ['G','R','S','T','W','Z','L','L1','L2','X','X1','Y','Y1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORCI')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'ORCC'; avec = bra2avec('ORCC')
   kSymbols = ['G','R','S','T','Y','Z','A','A1','X','X1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'ORCC')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'HEX'; avec = bra2avec('HEX1')
   kSymbols = ['G','A','H','K','L','M']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'HEX1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'HEX'; avec = bra2avec('HEX2')
   kSymbols = ['G','A','H','K','L','M']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'HEX2')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'RHL'; avec = bra2avec('RHL1')
   kSymbols = ['G','F','L','L1','Z','B','B1','P','P1','P2','Q','X']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'RHL1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'RHL'; avec = bra2avec('RHL2')
   kSymbols = ['G','F','L','Z','P','P1','Q','Q1']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'RHL2')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'MCL'; avec = bra2avec('MCL')
   kSymbols = ['G','A','C','D','D1','E','X','Y','Y1','Z','H','H1','H2','M','M1','M2']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'MCL')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC1')
   kSymbols = ['G','N','N1','L','M','Y','Y1','Z','F','F1','F2','F3','I','I1','X','X1','X2']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'MCLC1')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC3')
   kSymbols = ['G','I','M','N','N1','X','Z','F','F1','F2','H','H1','H2','Y','Y1','Y2','Y3']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'MCLC3')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC5')
   kSymbols = ['G','L','M','N','N1','X','Z','F','F1','F2','H','H1','H2','I','I1','Y','Y1','Y2','Y3']
   print_kvalues(crystalStructure, avec, kSymbols)
   # print('%s' % 'MCLC5')
   # print('%f %f %f' % (avec[0,0],avec[0,1],avec[0,2]))
   # print('%f %f %f' % (avec[1,0],avec[1,1],avec[1,2]))
   # print('%f %f %f' % (avec[2,0],avec[2,1],avec[2,2]))

