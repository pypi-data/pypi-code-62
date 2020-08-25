import numpy as np
import sympy as sym
from SOSTOOLSPy.oldconstructZ2 import oldconstructZ2

def monomials2(vartable,d):
    Z=[]
    d=d.astype(int)
    k=0
    for i in d:
        if k==0:
            Z=oldconstructZ2(vartable,int(i))
            k=k+1
        else:
            Z=np.concatenate((Z,oldconstructZ2(vartable,int(i))))
        
    return Z