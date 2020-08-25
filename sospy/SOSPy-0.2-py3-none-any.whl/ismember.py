#Ismember---Extract the index of the elements in symexpr.varname which are in cvartable as well

import numpy as np


def ismember(A,B):

    var=list(A)
    var=np.array(var).astype('str').tolist()
    var=np.asarray(var)
    nterm1=len(var)
    nterm2=len(B)
    idx=np.zeros((1,nterm1))
    k=0
    for i in range(nterm1):
        for j in range(nterm2):
            if var[i]==B[j]:
                idx[0][k]=j
                k+=1


    return idx 