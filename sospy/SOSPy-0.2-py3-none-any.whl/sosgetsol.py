import sympy as sym
from sympy import *
import numpy as np

def sosgetsol(sol,var):
    
    
    for i in range(len(sol.decvartable)):
        
        var=var.subs(sol.decvartable[i],sol.decvar[i])
    
    
    return var
