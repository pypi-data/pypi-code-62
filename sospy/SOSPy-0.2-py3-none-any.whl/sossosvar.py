import sympy as sym
import numpy as np

def sossosvar(prog,Z):
    
    var_holder = {}
    decvartable=[]
    for i in range(len(Z)**2):
        var_holder['coeff_' + str(i)]=sym.Symbol('coeff_%d'%prog.j)
        decvartable=np.append(decvartable,var_holder['coeff_' + str(i)])
        prog.j=prog.j+1
    locals().update(var_holder)
    
    var=0
    k=0
    for i in range(len(Z)):
        for j in range(len(Z)):
            var=var + Z[i]*(Z[j]*var_holder['coeff_' + str(k)])
            k=k+1
            
        
    
    prog.ndecvars=len(decvartable)
    prog.decvartable=np.concatenate((prog.decvartable,decvartable),axis=None)
    prog.decvar=np.concatenate((prog.decvar,decvartable),axis=None)

    
    return prog,var