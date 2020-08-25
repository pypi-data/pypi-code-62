import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from sympy import degree_list
from sympy import degree
from sympy import LT
from sympy import LM
from sympy import LC
from SOSTOOLSPy.getequation import getequation
from sympy import ImmutableMatrix as  Matrix
from collections import defaultdict
from SOSTOOLSPy.polystr import polystr
from sympy import SparseMatrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from sympy import sympify
from scipy.sparse import csr_matrix
from SOSTOOLSPy.max_kron import max_kron 
from scipy import sparse
from sympy import poly
from sympy import factor
from SOSTOOLSPy.findcommonZ import findcommonZ

def getconstraint2(Z):
    
    sizeZ=Z.shape[0]
    ZZ=Z +np.matlib.repmat(Z[0][:],sizeZ,1)
    
   
    #Creating a structure matrix M which will received the permutation matrices: R1, ..., Rn.
    
    Rn=[]    
    M = [Rn for i in range(sizeZ)]
    M[0]=np.eye(sizeZ, dtype=int)
    
    k=0
    R1=[]
    R2=np.eye(sizeZ, dtype=int)
    
    for i in np.arange(1,sizeZ):
        Ztemp=Z +np.matlib.repmat(Z[i][:],sizeZ,1)
        R1,R2,ZZ = findcommonZ(ZZ,Ztemp)
       
        for j in range(i):
            M[j] = np.matmul(M[j], R1)
         
        M[i]=R2
      
        
   
   
    Q=np.zeros((sizeZ,sizeZ))
    A=np.zeros((ZZ.shape[0],sizeZ**2))
    c=-1
    for i in range (sizeZ**2):
        r=np.mod(i,sizeZ)
        if r==0:
            c=c+1
        Q[r][c]=1
        j=r
        A[:,i]=(np.array([A[:,i]]).T+np.matmul(M[j].T,np.array([Q[j][:]]).T)).T[0]
        Q[r][c]=0

    
    return A,ZZ