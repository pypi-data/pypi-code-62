import numpy as np


def sosdecvar (prog,decvar):
    
    
    prog.decvar=np.append(prog.decvar,decvar)
    prog.ndecvars=len(prog.decvar)
    prog.decvartable=np.append(prog.decvartable,decvar)
    
    
    return prog