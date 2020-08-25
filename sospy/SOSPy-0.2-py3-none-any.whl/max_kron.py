# MAX_KRON-function--> Get a max element of the operation sum((Z == kron(ones(n,1), v)),2)

import numpy as np



def max_kron(Z,v):
    
    nmon,nvar=Z.shape
    x=np.kron(ones(nmon,1),v)
    x=x.astype('uint8')
    x=x.sum(axis=1)
    value=np.amax(x)
    index=np.argmax(x)
    
    return value, index