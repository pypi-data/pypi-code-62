import numpy as np
import sympy as sym
from sympy import degree_list,degree,LT,LM,LC,sympify
from sympy import matrix2numpy
from sympy.core.compatibility import as_int
from SOSTOOLSPy.getequation import getequation
from sympy import ImmutableMatrix as  Matrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from sympy import poly
from sympy import factor
from SOSTOOLSPy.monomials import monomials

def getconstraint(Z):
    
    sizeZ=Z.shape[0]
    ZZ=Z + np.matlib.repmat(Z[0],sizeZ,1).T
    ZZ=ZZ[0]
    
    #Creating a structure matrix M which will received the permutation matrices: R1, ..., Rn.
    
    Rn=[]    
    M = [Rn for i in range(sizeZ)]
    M[0]=np.eye(sizeZ, dtype=int)
    
    k=0
    R1=[]
    R2=np.eye(sizeZ, dtype=int)
    
    for i in np.arange(1,sizeZ):
        
        
        R1= np.concatenate((np.eye(sizeZ+k, dtype=int), np.zeros((sizeZ+k,1),dtype=int)), axis=1) 
        R2=np.concatenate((np.zeros((sizeZ,1),dtype=int),R2), axis=1)
        k=k+1
        ZZ=np.append(ZZ,ZZ[len(ZZ)-1]+1)
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