# SortNoRepeat --- Sort the elements os a matrix and return the result of this operetion 

import numpy as np

def sortNoRepeat(A,indices):
    Z=A
    nmon,nvar=Z.shape
    changed=np.ones((1,nvar))

    for k in range(nvar):
        for l in range(nmon):
            ind=int(indices[0][k])
            if int(changed[0][k])==1 and int(changed[0][ind])==1:
                Z_col=Z[l][k]
                Z[l][k]=Z[l][ind]
                Z[l][ind]=Z_col
                if l==nmon-1:
                    changed[0][k]=0
                    changed[0][ind]=0


    return Z