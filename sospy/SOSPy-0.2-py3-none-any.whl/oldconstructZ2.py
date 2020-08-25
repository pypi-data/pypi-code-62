import numpy as np
import sympy as sym
from sympy import degree_list,degree,LT,LM,LC,sympify
from sympy import matrix2numpy
from sympy.core.compatibility import as_int
from SOSTOOLSPy.getequation import getequation
from sympy import ImmutableMatrix as  Matrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from scipy.sparse import csr_matrix
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from sympy import poly
from sympy import factor
from numpy import matlib

def oldconstructZ2(vartable,d):
    
    

    ZZ=np.zeros((1, vartable)) 
    
    for i in range(vartable):
        ss=ZZ.shape[0]
        
        ZZ = np.matlib.repmat(ZZ,d+1,1)
        
        for j in range(d+1):
            
            for l in np.arange(ss*j,ss*j+ss):
               
                ZZ[l][i]=j
                
        sum_rows=ZZ.sum(axis=1)   
        nelements=len(sum_rows)
        index=-np.ones((1,nelements))
       
        k=0
        for j in range(nelements):    # Throw away invalid monomials
            if (sum_rows[j]<=d):
                index[0][k]=j
                k=k+1
        
        idx=-np.ones((1,k))
        idx=index[0][0:k]
        idx=idx.astype(int)
        
        Ztemp=np.zeros((len(idx),ZZ.shape[1]))
        
        for m in range(len(idx)):
            
            Ztemp[m][:]=ZZ[idx[m]][:]
        
        ZZ=Ztemp
        
        
    sum_rows=ZZ.sum(axis=1)   
    nelements=len(sum_rows)
    index=-np.ones((1,nelements))

    k=0
    for j in range(nelements):    # Throw away invalid monomials
        if (sum_rows[j]==d):
            index[0][k]=j
            k=k+1

    idx=-np.ones((1,k))
    idx=index[0][0:k]
    idx=idx.astype(int)

    Ztemp=np.zeros((len(idx),ZZ.shape[1]))

    for m in range(len(idx)):

        Ztemp[m][:]=ZZ[idx[m]][:]

    Z=Ztemp
       
    return Z