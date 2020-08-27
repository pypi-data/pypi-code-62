# pylint: disable=unused-variable

import numpy as np

def empty_list(length, dimensions=1):
    #Create tuple `Dimensions` long 
    a = (length,)
    for i in range(1,dimensions):
        a = a + (length,)
    
    #Return zeros with the shape of the tuple
    return (np.zeros(a)).tolist()