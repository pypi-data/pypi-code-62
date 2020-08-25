import numpy as np
from SOSTOOLSPy.oldconstructZ import oldconstructZ

def monomials(vartable,d):
    Z=[]
    d=d.astype(int)
    for i in d:
        Z=np.concatenate((Z,oldconstructZ(vartable,int(i))),axis=None) 
    return Z