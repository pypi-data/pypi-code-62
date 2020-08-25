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

def oldconstructZ(vartable,d):
    
    ZZ=csr_matrix((1, vartable), dtype=np.int8).toarray()

    for i in range(vartable):
        ss=len(ZZ)
        ZZ = np.matlib.repmat(ZZ,d+1,1)
        for j in range(d+1):
            ZZ[np.arange(ss*j,ss*j+ss)]=j

        sum_rows=ZZ.sum(axis=1)   
        nelements=len(sum_rows)
        index=np.zeros((1,nelements))
        k=0
        for j in range(nelements):    # Throw away invalid monomials
            if (sum_rows[j]<=d):
                index[0][k]=j
                k=k+1
        idx=np.zeros((1,k))
        idx=index[0:k] 
        idx=idx.astype(int)
        ZZ = ZZ[idx][:]

    sum_rows=ZZ[0].sum(axis=1)   
    nelements=len(sum_rows)
    index=np.zeros((1,nelements))

    k=0
    for l in range(nelements):    
        if (sum_rows[l]==d):
            index[0][k]=l
            k=k+1
    idx=np.zeros((1,k))
    idx=index[0][0:k] 
    idx=idx.astype(int)
    Z = ZZ[0][idx][:]
       
    return Z