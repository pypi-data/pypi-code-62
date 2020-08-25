# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict
from rescupy.utils import set_units as utils_set_units

class Cell:
   """
   cell class.
   
   Attributes
   ----------
   avec : 2D array
      Domain vectors.
   boundary : 1D array
      Boundary type for each face of the parallelepipedic domain.
   bravais : string
      Bravais lattice.
   grid : 1D array
      Number of grid points along each dimension.
   cres : float
      Grid resolution

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # default values
      defDict = {
         "avec"      : [0. for i in range(9)],
         "avecUnits" : "ang",
         "boundary"  : [0, 0, 0, 0, 0, 0],
         "bravais"   : None,
         "grid"      : None,
         "lres"      : None,
         "lresUnits" : "ang",
      }
      # required status
      reqDict = {
         "avec"     : True,
         "avecUnits": False,
         "boundary" : False,
         "bravais"  : False,
         "grid"     : False,
         "lres"     : False,
         "lresUnits": False,
      }
      
      init_from_dict(self, reqDict, defDict, inpDict)

      self.avec = np.array(self.avec).reshape((3,3))

      if self.bravais is None:
         self.bravais = self.get_bravais_lattice()
         
      if self.grid is None: 
         try: 
            if self.lresUnits != self.avecUnits:
               raise NameError('Inconsistent units between cell.avec and cell.lres.')
            lres = self.lres
            clen = self.lengths()
            self.grid = np.ceil(clen / lres).astype(int)
         except ValueError:
            raise NameError('Input file is missing a value for parameter cell.grid.')

      if self.lres is None: 
         try: 
            grid = inpDict['grid']
            clen = self.lengths()
            self.lres = np.mean(clen / grid)
            self.lresUnits = self.avecUnits
         except ValueError:
            raise NameError('Input file is missing a value for parameter cell.lres.')

      if isinstance(self.grid, list):
         self.grid = np.array(self.grid)

   def asdict(self):
      return utils_asdict(self)

   def set_units(self, units):
      return utils_set_units(self, units)

   def get_dx(self, axis):
      """
      Returns the grid node-to-node distance along a given direction.

      Parameters:
         axis (int): Lattice vector index.

      Returns: 
         dx (float): Node-to-node distance
      """
      return self.get_length(axis) / self.grid[axis]

   def get_grid(self, axis):
      """
      Returns the coordinates of the grid nodes along a given direction.

      Parameters:
         axis (int): Axis along which the grid node coordinates are sought.

      Returns: 
         x (ndarray): Numpy array containing the grid node coordinates.
      """
      n = self.grid[axis]
      u = np.zeros((n,3))
      u[:,axis] = np.array([i for i in range(1,n+1)]) / n
      x = np.matmul(u,self.avec)
      return x

   def get_length(self, axis):
      """
      Returns the length of a lattice vector.

      Parameters:
         axis (int): Lattice vector index.

      Returns: 
         l (float): Length of the lattice vector.
      """
      return np.linalg.norm(self.avec[axis,:])

   def get_lengths(self):
      """
      Returns the lengths of the lattice vectors.

      Parameters:

      Returns: 
         l (ndarray): Lengths of the lattice vectors.
      """
      return np.linalg.norm(self.avec, axis=1)

   def get_bravais_lattice(self, tol = 1e-3):
      return get3DCrystalStructure(self.avec, tol = tol)

   def get_standard_lattice(self, tol = 1e-3):
      if self.bravais is None:
         self.bravais = self.get_bravais_lattice(tol = tol)
      return getStandardPrimitiveCellVectors(self.bravais, self.avec, tol = tol)

   def lengths(self):
      avec = self.avec
      return np.linalg.norm(avec, axis=1)

   def reciprocal(self):
      avec = self.avec
      bvec = 2 * np.pi * np.linalg.inv(avec).T
      if self.avecUnits == "ang":
         bvecUnits = "invang"
      elif self.avecUnits == "bohr":
         bvecUnits = "invbohr"
      return bvec, bvecUnits

def get3DCrystalStructure(primitiveCellVectors, tol = 1e-3):
   """
   Return the crystal structure of given three linearly independent lattice vectors.

   Parameters
   ----------
   primitiveCellVectors: 2D array
      Lattice vectors (column-vectors).
      
   tol: scalar
      Tolerance.

   Returns
   ----------
   crystalStructure: string
      Crystal structure.
      
   """
   #
   # 14 cases:
   #     case 01: {'Cubic','CUB','SimpleCubic','SC','cP'})
   #     case 02: {'FaceCenteredCubic','FCC','cF'})
   #     case 03: {'BodyCenteredCubic','BCC','cI'})
   #     case 04: {'Tetragonal','TET','tP'})
   #     case 05: {'BodyCenteredTetragonal','BCT','tI'})
   #     case 06: {'Orthorhombic','ORC','oP'})
   #     case 07: {'FaceCenteredOrthorhombic','ORCF','oF'})
   #     case 08: {'BodyCenteredOrthorhombic','ORCI','oI'})
   #     case 09: {'CCenteredOrthorhombic','ORCC','oS'})
   #     case 10: {'Hexagonal','HEX','HCP','hP'})
   #     case 11: {'Rhombohedral','RHL','hR'})
   #     case 12: {'Monoclinic','MCL','mP'})
   #     case 13: {'CCenteredMonoclinic','MCLC','mS'})
   #     case 14: {'Triclinic','TRI','aP'})
   #
   v1 = primitiveCellVectors[0,:]
   v2 = primitiveCellVectors[1,:]
   v3 = primitiveCellVectors[2,:]
   a1 = np.linalg.norm(v1)
   a2 = np.linalg.norm(v2)
   a3 = np.linalg.norm(v3)
   a12 = np.dot(v1,v2)/a1/a2
   a23 = np.dot(v3,v2)/a2/a3
   a31 = np.dot(v1,v3)/a3/a1
   sqrt2 = np.sqrt(2.)
   sqrt3 = np.sqrt(3.)

   # SC
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         abs(a12-0) < tol and abs(a23-0) < tol and abs(a31-0) < tol:
      crystalStructure = 'CUB'
      return crystalStructure

   # FCC
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         abs(a12-1/2) < tol and abs(a23-1/2) < tol and abs(a31-1/2) < tol:
      crystalStructure = 'FCC'
      return crystalStructure

   # FCC-1
   if abs(a2/a3-1) < tol and abs(a3/a1-sqrt2/2) < tol and abs(a1/a2-sqrt2) < tol and \
         abs(2*a23-sqrt2*a31-sqrt2*a12+1) < tol and abs(sqrt2*a12-1) < tol and abs(sqrt2*a31-1) < tol:
      crystalStructure = 'FCC'
      return crystalStructure

   # FCC-2
   if abs(a3/a1-1) < tol and abs(a1/a2-sqrt2/2) < tol and abs(a2/a3-sqrt2) < tol and \
         abs(2*a31-sqrt2*a12-sqrt2*a23+1) < tol and abs(sqrt2*a23-1) < tol and abs(sqrt2*a12-1) < tol:
      crystalStructure = 'FCC'
      return crystalStructure

   # FCC-3
   if abs(a1/a2-1) < tol and abs(a2/a3-sqrt2/2) < tol and abs(a3/a1-sqrt2) < tol and \
         abs(2*a12-sqrt2*a23-sqrt2*a31+1) < tol and abs(sqrt2*a31-1) < tol and abs(sqrt2*a23-1) < tol:
      crystalStructure = 'FCC'
      return crystalStructure

   # BCC
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         abs(a12+1/3) < tol and abs(a23+1/3) < tol and abs(a31+1/3) < tol:
      crystalStructure = 'BCC'
      return crystalStructure

   # BCC-3
   if abs(a1/a2-1) < tol and abs(a2/a3-2/sqrt3) < tol and abs(a3/a1-sqrt3/2) < tol and \
         abs(a12-0) < tol and abs(a23-1/sqrt3) < tol and abs(a31-1/sqrt3) < tol:
      crystalStructure = 'BCC'
      return crystalStructure

   # BCC-1
   if abs(a2/a3-1) < tol and abs(a3/a1-2/sqrt3) < tol and abs(a1/a2-sqrt3/2) < tol and \
         abs(a23-0) < tol and abs(a31-1/sqrt3) < tol and abs(a12-1/sqrt3) < tol:
      crystalStructure = 'BCC'
      return crystalStructure

   # BCC-2
   if abs(a3/a1-1) < tol and abs(a1/a2-2/sqrt3) < tol and abs(a2/a3-sqrt3/2) < tol and \
         abs(a31-0) < tol and abs(a12-1/sqrt3) < tol and abs(a23-1/sqrt3) < tol:
      crystalStructure = 'BCC'
      return crystalStructure

   # Tetragonal
   if (abs(a1/a2-1) < tol or abs(a2/a3-1) < tol or abs(a3/a1-1) < tol) and \
         abs(a12-0) < tol and abs(a23-0) < tol and abs(a31-0) < tol:
      crystalStructure = 'TET'
      return crystalStructure

   # BodyCenteredTetragonal
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         (abs(a1/a2-a2/a1+a31/a2*a3-a23/a1*a3) < tol or abs(a2/a3-a3/a2+a12/a3*a1-a31/a2*a1) < tol  or abs(a3/a1-a1/a3+a23/a1*a2-a12/a3*a2) < tol) and \
         abs(a12+a23+a31+1) < tol:
      crystalStructure = 'BCT'
      return crystalStructure

   # BodyCenteredTetragonal-3
   if abs(a1/a2-1) < tol and \
         abs(a12-0) < tol and abs(2*a23-a2/a3) < tol and abs(2*a31-a1/a3) < tol:
      crystalStructure = 'BCT'
      return crystalStructure

   # BodyCenteredTetragonal-1
   if abs(a2/a3-1) < tol and \
         abs(a23-0) < tol and abs(2*a31-a3/a1) < tol and abs(2*a12-a2/a1) < tol:
      crystalStructure = 'BCT'
      return crystalStructure

   # BodyCenteredTetragonal-2
   if abs(a3/a1-1) < tol and \
         abs(a31-0) < tol and abs(2*a12-a1/a2) < tol and abs(2*a23-a3/a2) < tol:
      crystalStructure = 'BCT'
      return crystalStructure

   # Orthorhombic
   if abs(a12-0) < tol and abs(a23-0) < tol and abs(a31-0) < tol:
      crystalStructure = 'ORC'
      return crystalStructure

   # FaceCenteredOrthorhombic
   if abs(2*a12-a2/a1-a1/a2+a3/a2*a3/a1) < tol and abs(2*a23-a3/a2-a2/a3+a1/a3*a1/a2) < tol and abs(2*a31-a1/a3-a3/a1+a2/a1*a2/a3) < tol:
      crystalStructure = 'ORCF'
      return crystalStructure

   # FaceCenteredOrthorhombic-1
   if abs(4*a23*a2/a1*a3/a1-2*a31*a3/a1-2*a12*a2/a1+1) < tol and abs(2*a12*a2/a1-1) < tol and abs(2*a31*a3/a1-1) < tol:
      crystalStructure = 'ORCF'
      return crystalStructure

   # FaceCenteredOrthorhombic-2
   if abs(4*a31*a3/a2*a1/a2-2*a12*a1/a2-2*a23*a3/a2+1) < tol and abs(2*a23*a3/a2-1) < tol and abs(2*a12*a1/a2-1) < tol:
      crystalStructure = 'ORCF'
      return crystalStructure

   # FaceCenteredOrthorhombic-3
   if abs(4*a12*a1/a3*a2/a3-2*a23*a2/a3-2*a31*a1/a3+1) < tol and abs(2*a31*a1/a3-1) < tol and abs(2*a23*a2/a3-1) < tol:
      crystalStructure = 'ORCF'
      return crystalStructure

   # BodyCenteredOrthorhombic
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         abs(a12+a23+a31+1) < tol:
      crystalStructure = 'ORCI'
      return crystalStructure

   # BodyCenteredOrthorhombic-3
   if abs(a12-0) < tol and abs(2*a23-a2/a3) < tol and abs(2*a31-a1/a3) < tol:
      crystalStructure = 'ORCI'
      return crystalStructure

   # BodyCenteredOrthorhombic-1
   if abs(a23-0) < tol and abs(2*a31-a3/a1) < tol and abs(2*a12-a2/a1) < tol:
      crystalStructure = 'ORCI'
      return crystalStructure

   # BodyCenteredOrthorhombic-2
   if abs(a31-0) < tol and abs(2*a12-a1/a2) < tol and abs(2*a23-a3/a2) < tol:
      crystalStructure = 'ORCI'
      return crystalStructure

   # CCenteredOrthorhombic: SideCenteredOrthorhombic-3
   if abs(a1/a2-1) < tol and \
         abs(a23-0) < tol and abs(a31-0) < tol and \
         abs(abs(a12)-1/2) > tol:
      crystalStructure = 'ORCC'
      return crystalStructure

   # CCenteredOrthorhombic: SideCenteredOrthorhombic-1
   if abs(a2/a3-1) < tol and \
         abs(a31-0) < tol and abs(a12-0) < tol and \
         abs(abs(a23)-1/2) > tol:
      crystalStructure = 'ORCC'
      return crystalStructure

   # CCenteredOrthorhombic: SideCenteredOrthorhombic-2
   if abs(a3/a1-1) < tol and \
         abs(a12-0) < tol and abs(a23-0) < tol and \
         abs(abs(a31)-1/2) > tol:
      crystalStructure = 'ORCC'
      return crystalStructure

   # Hexagonal
   if abs(a1/a2-1) < tol and \
         abs(abs(a12)-1/2) < tol and abs(a23-0) < tol and abs(a31-0) < tol:
      crystalStructure = 'HEX'
      return crystalStructure
   elif abs(a2/a3-1) < tol and \
         abs(abs(a23)-1/2) < tol and abs(a31-0) < tol and abs(a12-0) < tol:
      crystalStructure = 'HEX'
      return crystalStructure
   elif abs(a3/a1-1) < tol and \
         abs(abs(a31)-1/2) < tol and abs(a12-0) < tol and abs(a23-0) < tol:
      crystalStructure = 'HEX'
      return crystalStructure

   # Rhombohedral
   if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
         abs(a12/a23-1) < tol and abs(a23/a31-1) < tol and abs(a31/a12-1) < tol:
      crystalStructure = 'RHL'
      return crystalStructure

   # Monoclinic
   if np.count_nonzero(abs(np.array([a12, a23, a31])-0.) < tol) == 2:
      crystalStructure = 'MCL'
      return crystalStructure

   # CCenteredMonoclinic: SideCenteredMonoclinic-3
   if abs(a1/a2-1) < tol and \
         abs(abs(a23)-abs(a31)) < tol:
      crystalStructure = 'MCLC'
      return crystalStructure

   # CCenteredMonoclinic: SideCenteredMonoclinic-1
   if abs(a2/a3-1) < tol and \
         abs(abs(a31)-abs(a12)) < tol:
      crystalStructure = 'MCLC'
      return crystalStructure

   # CCenteredMonoclinic: SideCenteredMonoclinic-2
   if abs(a3/a1-1) < tol and \
         abs(abs(a12)-abs(a23)) < tol:
      crystalStructure = 'MCLC'
      return crystalStructure

   # Triclinic
   crystalStructure = 'TRI'
   return crystalStructure

import numpy as np

def getStandardPrimitiveCellVectors(crystalStructure,primitiveCellVectors,tol=1e-3):
   """
   For 0D or 1D system,there is only 1, case.
   
   5 cases for 2D system:
       case 1: {'Square2D','SQU2D'}
       case 2: {'Rectangular2D','Rectangle2D','REC2D'}
       case 3: {'Hexagonal2D','Hexagon2D','HEX2D'}
       case 4: {'Rhombic2D','Rhombus2D','CenteredRectangular2D','RHO2D'}
       case 5: {'Oblique2D','OBL2D'}
   
   14 cases for 3D system:
       case 01: {'Cubic','CUB','SimpleCubic','SC','cP'})
       case 02: {'FaceCenteredCubic','FCC','cF'})
       case 03: {'BodyCenteredCubic','BCC','cI'})
       case 04: {'Tetragonal','TET','tP'})
       case 05: {'BodyCenteredTetragonal','BCT','tI'})
       case 06: {'Orthorhombic','ORC','oP'})
       case 07: {'FaceCenteredOrthorhombic','ORCF','oF'})
       case 08: {'BodyCenteredOrthorhombic','ORCI','oI'})
       case 09: {'CCenteredOrthorhombic','ORCC','oS'})
       case 10: {'Hexagonal','HEX','HCP','hP'})
       case 11: {'Rhombohedral','RHL','hR'})
       case 12: {'Monoclinic','MCL','mP'})
       case 13: {'CCenteredMonoclinic','MCLC','mS'})
       case 14: {'Triclinic','TRI','aP'})
   """
   primitiveCellVectors = primitiveCellVectors.transpose()
   v1 = primitiveCellVectors[:,0]
   v2 = primitiveCellVectors[:,1]
   v3 = primitiveCellVectors[:,2]
   a1 = np.linalg.norm(v1)
   a2 = np.linalg.norm(v2)
   a3 = np.linalg.norm(v3)
   a12 = np.dot(v1,v2)/a1/a2
   a23 = np.dot(v3,v2)/a2/a3
   a31 = np.dot(v1,v3)/a3/a1
   sqrt2 = np.sqrt(2.)
   sqrt3 = np.sqrt(3.)

   if crystalStructure == '0D':
      # 0D: isolate :: [10, 10, 10]
      spcv = primitiveCellVectors
   elif crystalStructure == '1D':
      # 1D: along z direction. c << a,b :: [10, 10, 1]
      # pcv = primitiveCellVectors
      I = np.argsort(-[a1, a2, a3]) # descending
      spcv = primitiveCellVectors[:,I]
   elif crystalStructure in ['Square2D','SQU2D']:
      # 2D1: along x-y plane. c >> a,b
      #     [[1, 0, 0]',[0,1,0]',[0, 0, 10]'] :: [1, 1, 10]
      #     analog: Tetragonal
      I = np.argsort([a1, a2, a3])
      spcv = primitiveCellVectors[:,I]
   elif crystalStructure in ['Rectangular2D','Rectangle2D','REC2D']:
      # 2D2: along x-y plane. c >> a,b
      #     [[1, 0, 0]',[0,2,0]',[0, 0, 10]'] :: [1, 1, 10]
      #     analog: Orthorhombic
      I = np.argsort([a1, a2, a3])
      spcv = primitiveCellVectors[:,I]
   elif crystalStructure in ['Hexagonal2D','Hexagon2D','HEX2D']:
      # 2D3: along x-y plane. c >> a,b
      #     [[1/2, -sqrt3/2 0]',[1/2,sqrt3/2,0]',[0, 0, 10]'] :: [1, 1, 10]
      #     analog: Hexagonal
      I = np.argsort([a1, a2, a3])
      spcv = primitiveCellVectors[:,I]
      if np.linalg.norm(spcv[:,0]+spcv[:,1]) > np.linalg.norm(spcv[:,0]-spcv[:,1]):
         spcv[:,1] = -spcv[:,1]
   elif crystalStructure in ['Rhombic2D','Rhombus2D','CenteredRectangular2D','RHO2D']:
      # 2D4:  along x-y plane. c >> a,b
      #     [[1/2, -2/2 0]',[1/2,2/2,0]',[0, 0, 10]'] :: [1, 2 10]
      #     analog: CCenteredOrthorhombic
      I = np.argsort([a1, a2, a3])
      spcv = primitiveCellVectors[:,I]
      if np.linalg.norm(spcv[:,0]+spcv[:,1]) > np.linalg.norm(spcv[:,0]-spcv[:,1]):
         spcv[:,1] = -spcv[:,1]
   elif crystalStructure in ['Oblique2D','OBL2D']:
      # 2D5:  along x-y plane. c >> a,b
      #     [[2 0, 0]',[3*cos(pi/5),3*sin(pi/5),0]',[0, 0, 10]'] :: [2 3 10]
      #     analog: 'Monoclinic'
      I = np.argsort([a1, a2, a3])
      spcv = primitiveCellVectors[:,I]
      if dot(spcv[:,0],spcv[:,1]) < 0:
         spcv[:,0] = -spcv[:,0]
   elif crystalStructure in ['Cubic','CUB','SimpleCubic','SC','cP']:
      # 1: ucv = pcv = [[1, 0, 0]',[0, 1, 0]',[0, 0, 1]']
      ucv = primitiveCellVectors
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = sucv
   elif crystalStructure in ['FaceCenteredCubic','FCC','cF']:
      # 2: pcv = [[0, 1/2, 1/2]',[1/2,0,1/2]',[1/2, 1/2, 0]']
      #    ucv = [[1, 0, 0]',[0, 1, 0]',[0, 0, 1]']
      pcv = primitiveCellVectors
      if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
            abs(a12-1/2) < tol and abs(a23-1/2) < tol and abs(a31-1/2) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a2/a3-1) < tol and abs(a3/a1-sqrt2/2) < tol and abs(a1/a2-sqrt2) < tol and \
            abs(2*a23-sqrt2*a31-sqrt2*a12+1) < tol and abs(sqrt2*a12-1) < tol and abs(sqrt2*a31-1) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a3/a1-1) < tol and abs(a1/a2-sqrt2/2) < tol and abs(a2/a3-sqrt2) < tol and \
            abs(2*a31-sqrt2*a12-sqrt2*a23+1) < tol and abs(sqrt2*a23-1) < tol and abs(sqrt2*a12-1) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[0, 1, 0],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a1/a2-1) < tol and abs(a2/a3-sqrt2/2) < tol and abs(a3/a1-sqrt2) < tol and \
            abs(2*a12-sqrt2*a23-sqrt2*a31+1) < tol and abs(sqrt2*a31-1) < tol and abs(sqrt2*a23-1) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[1/2,0,1/2],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[0, 1/2, 1/2],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
   elif crystalStructure in ['BodyCenteredCubic','BCC','cI']:
      # 3: pcv = [[-1/2, 1/2, 1/2]',[1/2,-1/2,1/2]',[1/2, 1/2, -1/2]']
      #    ucv = [[1, 0, 0]',[0, 1, 0]',[0, 0, 1]']
      pcv = primitiveCellVectors
      if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
            abs(a12+1/3) < tol and abs(a23+1/3) < tol and abs(a31+1/3) < tol:
         ucv = np.linalg.inv(np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a1/a2-1) < tol and abs(a2/a3-2/sqrt3) < tol and abs(a3/a1-sqrt3/2) < tol and \
            abs(a12-0) < tol and abs(a23-1/sqrt3) < tol and abs(a31-1/sqrt3) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[0, 1, 0],[1/2, 1/2, 1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a2/a3-1) < tol and abs(a3/a1-2/sqrt3) < tol and abs(a1/a2-sqrt3/2) < tol and \
            abs(a23-0) < tol and abs(a31-1/sqrt3) < tol and abs(a12-1/sqrt3) < tol:
         ucv = np.linalg.inv(np.array([[1/2, 1/2, 1/2],[0, 1, 0],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a3/a1-1) < tol and abs(a1/a2-2/sqrt3) < tol and abs(a2/a3-sqrt3/2) < tol and \
            abs(a31-0) < tol and abs(a12-1/sqrt3) < tol and abs(a23-1/sqrt3) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[1/2, 1/2, 1/2],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
   elif crystalStructure in ['Tetragonal','TET','tP']:
      # 4: ucv = pcv = [[1, 0, 0]',[0, 1, 0]',[0, 0, 5]']
      ucv = primitiveCellVectors
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = sucv
   elif crystalStructure in ['BodyCenteredTetragonal','BCT','tI']:
      # 5: pcv = [[-1/2, 1/2, 5/2]',[1/2,-1/2,5/2]',[1/2, 1/2, -5/2]']
      #    ucv = [[1, 0, 0]',[0, 1, 0]',[0, 0, 5]']
      pcv = primitiveCellVectors
      if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and \
            (abs(a1/a2-a2/a1+a31/a2*a3-a23/a1*a3) < tol or abs(a2/a3-a3/a2+a12/a3*a1-a31/a2*a1) < tol or \
               abs(a3/a1-a1/a3+a23/a1*a2-a12/a3*a2) < tol) and abs(a12+a23+a31+1) < tol:
         ucv = np.linalg.inv(np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a1/a2-1) < tol and \
            abs(a12-0) < tol and abs(2*a23-a2/a3) < tol and abs(2*a31-a1/a3) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[0, 1, 0],[1/2, 1/2, 1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a2/a3-1) < tol and \
            abs(a23-0) < tol and abs(2*a31-a3/a1) < tol and abs(2*a12-a2/a1) < tol:
         ucv = np.linalg.inv(np.array([[1/2, 1/2, 1/2],[0, 1, 0],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a3/a1-1) < tol and \
            abs(a31-0) < tol and abs(2*a12-a1/a2) < tol and abs(2*a23-a3/a2) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[1/2, 1/2, 1/2],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
   elif crystalStructure in ['Orthorhombic','ORC','oP']:
      # 6: ucv = pcv = [[1, 0, 0]',[0, 2 0]',[0, 0, 3]']
      ucv = primitiveCellVectors
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = sucv
   elif crystalStructure in ['FaceCenteredOrthorhombic','ORCF','oF']:
      # 7: pcv = [[0, 2/2 3/2]',[1/2,0,3/2]',[1/2, 2/2 0]']
      #    ucv = [[1, 0, 0]',[0, 2 0]',[0, 0, 3]']
      pcv = primitiveCellVectors
      if abs(2*a12-a2/a1-a1/a2+a3/a2*a3/a1) < tol and abs(2*a23-a3/a2-a2/a3+a1/a3*a1/a2) < tol and \
         abs(2*a31-a1/a3-a3/a1+a2/a1*a2/a3) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(4*a23*a2/a1*a3/a1-2*a31*a3/a1-2*a12*a2/a1+1) < tol and abs(2*a12*a2/a1-1) < tol and \
         abs(2*a31*a3/a1-1) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(4*a31*a3/a2*a1/a2-2*a12*a1/a2-2*a23*a3/a2+1) < tol and abs(2*a23*a3/a2-1) < tol and \
         abs(2*a12*a1/a2-1) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[0, 1, 0],[1/2, 1/2, 0]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(4*a12*a1/a3*a2/a3-2*a23*a2/a3-2*a31*a1/a3+1) < tol and abs(2*a31*a1/a3-1) < tol and \
         abs(2*a23*a2/a3-1) < tol:
         ucv = np.linalg.inv(np.array([[0, 1/2, 1/2],[1/2,0,1/2],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[0, 1/2, 1/2],[1/2,0,1/2],[1/2, 1/2, 0]]).T)
   elif crystalStructure in ['BodyCenteredOrthorhombic','ORCI','oI']:
      # 8: pcv = [[-1/2, 2/2 3/2]',[1/2,-2/2,3/2]',[1/2, 2/2 -3/2]']
      #    ucv = [[1, 0, 0]',[0, 2 0]',[0, 0, 3]']
      pcv = primitiveCellVectors
      if abs(a1/a2-1) < tol and abs(a2/a3-1) < tol and abs(a3/a1-1) < tol and abs(a12+a23+a31+1) < tol:
         ucv = np.linalg.inv(np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a12-0) < tol and abs(2*a23-a2/a3) < tol and abs(2*a31-a1/a3) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[0, 1, 0],[1/2, 1/2, 1/2]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a23-0) < tol and abs(2*a31-a3/a1) < tol and abs(2*a12-a2/a1) < tol:
         ucv = np.linalg.inv(np.array([[1/2, 1/2, 1/2],[0, 1, 0],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a31-0) < tol and abs(2*a12-a1/a2) < tol and abs(2*a23-a3/a2) < tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[1/2, 1/2, 1/2],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[-1/2, 1/2, 1/2],[1/2,-1/2,1/2],[1/2, 1/2, -1/2]]).T)
   elif crystalStructure in ['CCenteredOrthorhombic','ORCC','oS']:
      # 9: pcv = [[1/2, -2/2 0]',[1/2,2/2,0]',[0, 0, 3]']
      #    ucv = [[1, 0, 0]',[0, 2 0]',[0, 0, 3]']
      pcv = primitiveCellVectors
      if abs(a1/a2-1) < tol and abs(a23-0) < tol and abs(a31-0) < tol and abs(abs(a12)-1/2) > tol:
         ucv = np.linalg.inv(np.array([[1/2, -1/2, 0],[1/2,1/2,0],[0, 0, 1]]).T)
         ucv = np.matmul(pcv, ucv)
      elif abs(a2/a3-1) < tol and abs(a31-0) < tol and abs(a12-0) < tol and abs(abs(a23)-1/2) > tol:
         ucv = np.linalg.inv(np.array([[1, 0, 0],[0, 1/2, -1/2],[0, 1/2,1/2]]).T)
         ucv = np.matmul(pcv, ucv)
         ucv = ucv[:,[1,2,0]]
      elif abs(a3/a1-1) < tol and abs(a12-0) < tol and abs(a23-0) < tol and abs(abs(a31)-1/2) > tol:
         ucv = np.linalg.inv(np.array([[-1/2, 0, 1/2],[0, 1, 0],[1/2, 0, 1/2]]).T)
         ucv = np.matmul(pcv, ucv)
         ucv = ucv[:,[2,0,1]]
      sucv = getStandardUnitCellVectors(crystalStructure,ucv,tol)
      spcv = np.matmul(sucv, np.array([[1/2, -1/2, 0],[1/2,1/2,0],[0, 0, 1]]).T)
   elif crystalStructure in ['Hexagonal','HEX','HCP','hP']:
      # 10: ucv = pcv = [[1/2, -sqrt3/2 0]',[1/2,sqrt3/2,0]',[0, 0, 3]']
      pcv = primitiveCellVectors
      if abs(1/2-abs(a12)) <= tol:
         spcv = pcv
      elif abs(1/2-abs(a23)) <= tol:
         spcv = pcv[:,[1,2,0]]
      elif abs(1/2-abs(a31)) <= tol:
         spcv = pcv[:,[2,0,1]]
      if np.linalg.norm(spcv[:,0]+spcv[:,1]) > np.linalg.norm(spcv[:,0]-spcv[:,1]):
         spcv[:,1] = -spcv[:,1]
      if np.linalg.det(spcv) < 0:
         spcv[:,2] = -spcv[:,2]
   elif crystalStructure in ['Rhombohedral','RHL','hR']:
      # 11: ucv = pcv = [[cos(pi/5) -sin(pi/5) 0]',[cos(pi/5) sin(pi/5),0]',
      #      [cos(2*pi/5)/cos(pi/5),0,np.sqrt(1-(cos(2*pi/5)/cos(pi/5))^2)]']
      pcv = primitiveCellVectors
      if np.linalg.det(pcv) > 0:
         spcv = pcv
      else:
         spcv = pcv[:,[0,2,1]]
   elif crystalStructure in ['Monoclinic','MCL','mP']:
      # 12: ucv = pcv = [[1, 0, 0]',[0, 2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      pcv = primitiveCellVectors
      if abs(a31) <= tol and abs(a12) <= tol:
         spcv = pcv
      elif abs(a12) <= tol and abs(a23) <= tol:
         spcv = pcv[:,[1,2,0]]
      elif abs(a23) <= tol and abs(a31) <= tol:
         spcv = pcv[:,[2,0,1]]
      if np.linalg.norm(spcv[:,1]) > np.linalg.norm(spcv[:,2]):
         spcv[:,[1, 2]] = spcv[:,[2, 1]]
      if np.dot(spcv[:,1],spcv[:,2]) < 0:
         spcv[:,2] = -spcv[:,2]
      if np.linalg.det(spcv) < 0:
         spcv[:,0] = -spcv[:,0]
   elif crystalStructure in ['CCenteredMonoclinic','MCLC','mS']:
      # 13: pcv = [[1/2, 2/2 0]',[-1/2, 2/2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      #     ucv = [[1, 0, 0]',[0, 2 0]',[0,3*cos(pi/5),3*sin(pi/5)]']
      pcv = primitiveCellVectors
      if abs(1-a1/a2) <= tol and \
            abs(abs(a23)-abs(a31)) < tol:
         spcv = pcv
      elif abs(1-a2/a3) <= tol and \
            abs(abs(a31)-abs(a12)) <= tol:
         spcv = pcv[:,[1,2,0]]
      elif abs(1-a3/a1) <= tol and \
            abs(abs(a12)-abs(a23)) <= tol:
         spcv = pcv[:,[2,0,1]]
      if np.dot(spcv[:,0],spcv[:,2]) < 0:
         spcv[:,0] = -spcv[:,0]
      if np.dot(spcv[:,1],spcv[:,2]) < 0:
         spcv[:,1] = -spcv[:,1]
      if np.linalg.det(spcv) < 0:
         spcv = spcv[:,[1,0,2]]
   elif crystalStructure in ['Triclinic','TRI','aP']:
      # 14: ucv = pcv = [[1, 0, 0]',[2*cos(pi/3),2*sin(pi/3),0]',[3*cos(pi/4),
      #      3/sin(pi/3)*(cos(pi/5)-cos(pi/4)*cos(pi/3)),
      #      3/sin(pi/3)*np.sqrt(1-(cos(pi/5))^2-(cos(pi/4))^2-(cos(pi/3))^2
      #      + 2*cos(pi/5)*cos(pi/4)*cos(pi/3))]'] :: [1, 2 3],[pi/5,pi/4,pi/3]
      kpcv = np.linalg.inv(primitiveCellVectors).transpose()
      a = np.linalg.norm(kpcv[:,0])
      b = np.linalg.norm(kpcv[:,1])
      c = np.linalg.norm(kpcv[:,2])
      kalpha = np.dot(kpcv[:,1],kpcv[:,2])/b/c
      kbeta = np.dot(kpcv[:,2],kpcv[:,0])/c/a
      kgamma = np.dot(kpcv[:,0],kpcv[:,1])/a/b
      # making all signs of them same
      if kalpha*kbeta > 0:
         if kbeta*kgamma > 0:
            tmp = None
            # +++ or ---
         else:
            # ++- or --+
            kpcv[:,2] = -kpcv[:,2]
      else:
         if kbeta*kgamma > 0:
            # +-- or -++
            kpcv[:,0] = -kpcv[:,0]
         else:
            # +-+ or -+-
            kpcv[:,1] = -kpcv[:,1]
      # making the abs(kgamma) the smallest
      I = np.argsort(-[abs(kalpha),abs(kbeta),abs(kgamma)]) # descending
      kpcv = kpcv[:,I]
      spcv = np.linalg.inv(kpcv).transpose()
   else:
      # user defined crystal structure
      spcv = primitiveCellVectors
      
   standardPrimitiveCellVectors = spcv.transpose()
   return standardPrimitiveCellVectors

def getStandardUnitCellVectors(crystalStructure,unitCellVectors,tol):
   ucv = unitCellVectors
   u1 = np.linalg.norm(ucv[:,0])
   u2 = np.linalg.norm(ucv[:,1])
   u3 = np.linalg.norm(ucv[:,2])
   if crystalStructure in ['Cubic','CUB','SimpleCubic','SC','cP','FaceCenteredCubic','FCC','cF','BodyCenteredCubic','BCC','cI']:
      sucv = ucv
      if np.linalg.det(sucv) < 0:
         sucv = sucv[:,[1,0,2]]
   elif crystalStructure in ['Tetragonal','TET','tP','BodyCenteredTetragonal','BCT','tI']:
      if abs(1-u1/u2) <= tol:
         sucv = ucv
      elif abs(1-u2/u3) <= tol:
         sucv = ucv[:,[1,2,0]]
      elif abs(1-u3/u1) <= tol:
         sucv = ucv[:,[2,0,1]]
      if np.linalg.det(sucv) < 0:
         sucv = sucv[:,[1,0,2]]
   elif crystalStructure in ['Orthorhombic','ORC','oP','FaceCenteredOrthorhombic','ORCF','oF','BodyCenteredOrthorhombic','ORCI','oI']:
      I = np.argsort([u1, u2, u3])
      sucv = ucv[:,I]
      if np.linalg.det(sucv) < 0:
         sucv[:,2] = -sucv[:,2]
   elif crystalStructure in ['CCenteredOrthorhombic','ORCC','oS']:
      if u1 < u2:
         sucv = ucv
      else:
         sucv = ucv[:,[1,0,2]]
      if np.linalg.det(sucv) < 0:
         sucv[:,2] = -sucv[:,2]
   standardUnitCellVectors = sucv
   return standardUnitCellVectors

###########
# testing #
###########

def bra2avec(bra):
   #BRA2AVEC Summary of this function goes here
   #   Detailed explanation goes here
   # rot = rand(3); [rot,~]=qr(rot,0)
   pi = np.pi
   rot = np.array([[-0.612200019964379, 0.598061781627136, 0.517236155844301],
   [-0.784920533612324, -0.380695311210428, -0.488846433899380],
   [-0.095450989881504, -0.705261076041611,  0.702492649891278]])
   noteye = np.logical_not(np.eye(3)).astype(np.float)
   if bra == 'CUB':
      avec = np.matmul(np.eye(3), rot) # 'CUB'
   elif bra == 'FCC':
      avec = np.matmul(noteye, rot) # 'FCC'
   elif bra == 'BCC':
      avec = np.matmul((noteye-np.eye(3)), rot) # 'BCC'
   elif bra == 'RHL1':
      avec = np.array([[np.cos(0/180*pi)*np.sin(30/180*pi), np.sin(0/180*pi)*np.sin(30/180*pi), np.cos(30/180*pi)],
         [np.cos(120/180*pi)*np.sin(30/180*pi), np.sin(120/180*pi)*np.sin(30/180*pi), np.cos(30/180*pi)],         
         [np.cos(240/180*pi)*np.sin(30/180*pi), np.sin(240/180*pi)*np.sin(30/180*pi), np.cos(30/180*pi)]])
      avec = np.matmul(avec, rot) # 'RHL1'
   elif bra == 'RHL2':
      avec = np.array([[np.cos(0/180*pi)*np.sin(60/180*pi), np.sin(0/180*pi)*np.sin(60/180*pi), np.cos(60/180*pi)],
         [np.cos(120/180*pi)*np.sin(60/180*pi), np.sin(120/180*pi)*np.sin(60/180*pi), np.cos(60/180*pi)],
         [np.cos(240/180*pi)*np.sin(60/180*pi), np.sin(240/180*pi)*np.sin(60/180*pi), np.cos(60/180*pi)]])
      avec = np.matmul(avec, rot) # 'RHL2'
   elif bra == 'HEX1':
      avec = np.array([[np.cos(0/180*pi), np.sin(0/180*pi), 0],
         [np.cos(120/180*pi), np.sin(120/180*pi), 0],
         [0, 0, 2]])
      avec = np.matmul(avec, rot) # 'HEX'
   elif bra == 'HEX2':
      avec = np.array([[np.cos(0/180*pi), np.sin(0/180*pi), 0],
         [np.cos(60/180*pi), np.sin(60/180*pi), 0],
         [0, 0, 2]])
      avec = np.matmul(avec, rot) # 'HEX'
   elif bra == 'TET1':
      avec = np.matmul(np.diag([1,1,2]), rot) # 'TET'
   elif bra == 'TET2':
      avec = np.matmul(np.diag([2,1,2]), rot) # 'TET'
   elif bra == 'BCT1':
      avec = np.matmul((noteye-np.eye(3)) * np.array([2,2,1]), rot) # 'BCT1'
   elif bra == 'BCT2':
      avec = np.matmul((noteye-np.eye(3)) * np.array([1,1,2]), rot) # 'BCT2'
   elif bra == 'ORC':
      avec = np.matmul(np.diag([1,2,3]), rot) # 'ORC'
   elif bra == 'ORCF1':
      avec = np.matmul(noteye * np.array([1,2,3]), rot) # 'ORCF1'
   elif bra == 'ORCF2':
      avec = np.matmul(noteye * np.array([1,1.1,1.2]), rot) # 'ORCF2'
   elif bra == 'ORCF3':
      avec = np.matmul(noteye * np.array([1,np.sqrt(4/3),2]), rot) # 'ORCF3'
   elif bra == 'ORCI':
      avec = np.matmul((noteye-np.eye(3)) * np.array([1,2,3]), rot) # 'ORCI'
   elif bra == 'ORCC':
      avec = np.array([[1, -1, 0], [1, 1, 0], [0, 0, 1]])
      avec = np.matmul(avec * np.array([1,2,3]), rot) # 'ORCC'
   elif bra == 'MCL':
      alpha = pi/5
      avec = np.array([[1, 0, 0], [0, 1, 0], [0, np.cos(alpha), np.sin(alpha)]])
      avec = np.matmul(avec * np.array([[1,2,3]]).transpose(), rot) # 'MCL'
   elif bra == 'MCLC1':
      alpha = pi/2*0.9
      avec = np.matmul([[1, 2, 0], [-1, 2, 0], [0, 5*np.cos(alpha), 5*np.sin(alpha)]], rot) # 'MCLC1'
   elif bra == 'MCLC2':
      alpha = pi/2*0.1
      avec = np.matmul([[1, 1, 0], [-1, 1, 0], [0, 5*np.cos(alpha), 5*np.sin(alpha)]], rot) # 'MCLC2'
   elif bra == 'MCLC3':
      avec = np.matmul([[5.97357258101562, 3.45227203834125, 0.00000000000000],
         [-5.97357258101562, 3.45227203834125, 0.00000000000000],
         [0.00000000000000, 2.27661214292493, 6.80081526960862]], rot) # 'MCLC3'
   elif bra == 'MCLC4':
      alpha = pi/2*0.15160094
      avec = np.matmul([[1, 2, 0], [-1, 2, 0], [0, 5*np.cos(alpha), 5*np.sin(alpha)]], rot) # 'MCLC4'
   elif bra == 'MCLC5':
      avec = np.matmul([[5.40176783775381, 4.52407218161051, 0.00000000000000],
         [-5.40176783775381, 4.52407218161051, 0.00000000000000],
         [0.00000000000000, 4.51116525071579, 4.56749911424154]], rot) # 'MCLC5'
   return avec

def print_all_bra2avec():
   perm = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]

   crystalStructure = 'CUB'; avec = bra2avec('CUB')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','X','M','R']

   crystalStructure = 'FCC'; avec = bra2avec('FCC')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','K','L','U','W','X']

   crystalStructure = 'BCC'; avec = bra2avec('BCC')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','H','P','N']

   crystalStructure = 'TET'; avec = bra2avec('TET1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','A','M','R','X','Z']

   crystalStructure = 'TET'; avec = bra2avec('TET2')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','A','M','R','X','Z']

   crystalStructure = 'BCT'; avec = bra2avec('BCT1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','M','N','P','X','Z','Z1']

   crystalStructure = 'BCT'; avec = bra2avec('BCT2')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','N','P','X','Z','S','S1','Y','Y1']

   crystalStructure = 'ORC'; avec = bra2avec('ORC')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','R','S','T','U','X','Y','Z']

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','L','T','Y','Z','A','A1','X','X1']

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF2')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','L','X','Y','Z','C','C1','D','D1','H','H1']

   crystalStructure = 'ORCF'; avec = bra2avec('ORCF3')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','L','T','Y','Z','A','A1','X','X1']

   crystalStructure = 'ORCI'; avec = bra2avec('ORCI')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','R','S','T','W','Z','L','L1','L2','X','X1','Y','Y1']

   crystalStructure = 'ORCC'; avec = bra2avec('ORCC')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','R','S','T','Y','Z','A','A1','X','X1']

   crystalStructure = 'HEX'; avec = bra2avec('HEX1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','A','H','K','L','M']

   crystalStructure = 'HEX'; avec = bra2avec('HEX2')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','A','H','K','L','M']

   crystalStructure = 'RHL'; avec = bra2avec('RHL1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','F','L','L1','Z','B','B1','P','P1','P2','Q','X']

   crystalStructure = 'RHL'; avec = bra2avec('RHL2')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','F','L','Z','P','P1','Q','Q1']

   crystalStructure = 'MCL'; avec = bra2avec('MCL')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','A','C','D','D1','E','X','Y','Y1','Z','H','H1','H2','M','M1','M2']

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC1')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','N','N1','L','M','Y','Y1','Z','F','F1','F2','F3','I','I1','X','X1','X2']

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC3')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','I','M','N','N1','X','Z','F','F1','F2','H','H1','H2','Y','Y1','Y2','Y3']

   crystalStructure = 'MCLC'; avec = bra2avec('MCLC5')
   for i in range(0, len(perm)):
      avecp = avec[perm[i],:]
      print(get3DCrystalStructure(avecp))
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecp.flatten(order='F').tolist()))
      avecstd = getStandardPrimitiveCellVectors(crystalStructure, avecp)
      print("%f %f %f %f %f %f %f %f %f " % tuple(avecstd.flatten(order='F').tolist()))
   kSymbols = ['G','L','M','N','N1','X','Z','F','F1','F2','H','H1','H2','I','I1','Y','Y1','Y2','Y3']

