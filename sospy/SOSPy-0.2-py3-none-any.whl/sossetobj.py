# SOSSETOBJ --- Set the objective function of an SOS program. 
# SOSP = sossetobj(SOSP,EXPR)
# Given a sum of squares program SOSP and an expression EXPR, SOSSETOBJ
# makes EXPR the objective function of the sum of squares program SOSP, 
# i.e., EXPR will be minimized.

import sympy as sym
import numpy as np

def sossetobj(sos,obj):
    if sos.nconstraint>1:
        for i in range(len(sos.decvartable2)):
            if obj.coeff(sos.decvartable2[i])!=0:
                sos.ccon[i][0]=obj.coeff(sos.decvartable2[i])
    
    elif sos.nconstraint==1:
        sos.obj=np.append(sos.obj,obj)
        
    return sos