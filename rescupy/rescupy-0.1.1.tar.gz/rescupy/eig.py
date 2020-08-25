# -*- coding: utf-8 -*-
"""
Created on 2020-05-11

@author: Vincent Michaud-Rioux
"""

import numpy as np
from rescupy.utils import asdict as utils_asdict
from rescupy.utils import init_from_dict

class Eig:
   """
   eig class.
   
   Attributes
   ----------
   algo : string
      Algorithm.
   jobz : string
      If jobz = 'v', eigenvectors are calculated; only eigenvalues are returned otherwise.
   uplo : string
      If uplo = 'u', the upper triangular part of the matrices are referenced; if uplo = 'l', the upper triangular part of the matrices are referenced.
   range : string
      If range = 'a', all eigenvalues are computed; if range = 'i', the eigenvalues with index in the interval (il, iu) are computed; if range = 'v', the eigenvalues with index in the interval (vl, vu) are computed.
   ibtype : integer
      Eigenvalue problem type; if ibtype = 1, solve A*x = (lambda)*B*x; if ibtype = 2, solve A*B*x = (lambda)*x; if ibtype = 3, solve B*A*x = (lambda)*x.
   il : integer
      Lower index bound.
   iu : integer
      Upper index bound.
   lwork : integer
      Workspace size.
   reduAlgo : integer
      Switch between triangular inverse (1) and ScaLAPCK's sygst (2). 
   vl : float
      Lower value bound.
   vu : float
      Upper value bound.
   abstol : float
      The absolute error tolerance for the eigenvalues.
   orfac : float
      Specifies which eigenvectors should be reorthogonalized.
   trgtband : 1D array
      Target bands (must satisfy convergence criteria).
   inclband : 1D array
      Included bands (do not necessarily satisfy convergence criteria).

   Methods
   -------
   
   Remarks
   ---

   """
   def __init__(self, inpDict = {}):
      # required status
      reqDict = {
         "algo": False,
         # "jobz": False,
         # "uplo": False,
         # "range": False,
         # "ibtype": False,
         "reduAlgo": False,
         # "il": False,
         # "iu": False,
         "lwork": False,
         "orfac": False,
         "abstol": False,
         "trgtband": False,
         "inclband": False,
      }    
      # default values
      defDict = {
         "algo": "x",
         # "jobz": "n", 
         # "uplo": "u", 
         # "range": "a",
         # "ibtype": 1., 
         "reduAlgo": 2,
         # "il": 0, 
         # "iu": 0, 
         "lwork": -1,
         "orfac": 1.0e-6,
         "abstol": 1.0e-15,
         "trgtband": None,
         "inclband": None,
      }    
      
      init_from_dict(self, reqDict, defDict, inpDict)

   def asdict(self):
      return utils_asdict(self)