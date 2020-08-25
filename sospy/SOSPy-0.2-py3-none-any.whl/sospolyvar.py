import sympy as sym
import numpy as np

def sospolyvar(prog,monomials):
    
    var_holder = {}
    decvartable=[]
    for i in range(len(monomials)):
        var_holder['coeff_' + str(i)]=sym.Symbol('coeff_%d'%prog.j)
        decvartable=np.append(decvartable,var_holder['coeff_' + str(i)])
        prog.j=prog.j+1
    locals().update(var_holder)
    
    var=0
    for i in range(len(monomials)):
        var=var+var_holder['coeff_' + str(i)]*monomials[i]
        
    
    prog.ndecvars=len(decvartable)
    prog.decvartable=np.concatenate((prog.decvartable,decvartable),axis=None)
    prog.decvar=np.concatenate((prog.decvar,decvartable),axis=None)
    
    return prog,var