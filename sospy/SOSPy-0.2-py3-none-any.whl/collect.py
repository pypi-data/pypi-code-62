#Collect symexpr = g(c)*h(x) + g0 where x are the vars in vartable,
#c are the decision variables, and h(x) is a vector of monoms.
#in the actual polynomial vars.  Use this to find unique
#monomials in the polynomial variables.

import numpy as np
from typing import NamedTuple
import sympy as sym
from sympy import LT,LM,degree,degree_list
from dataclasses import dataclass
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
    
    
def collect(symexpr):

    #Create the matrix h
    ptemp=symexpr.polynomial
    h=zeros(symexpr.nterms,1)
    j=0
    for j in range(symexpr.nterms):
        h[j]=LM(ptemp)
        ptemp=ptemp-LT(ptemp)
    #Create the matrix g
    ptemp=symexpr.polynomial
    g=zeros(symexpr.nterms,1)
    j=0
    for j in range(symexpr.nterms):
        mon_coeff=LT(ptemp)
        mon=LM(ptemp)
        g[j]= mon_coeff/mon
        ptemp=ptemp-LT(ptemp)
    #Create the value g0
    g0=zeros(1,1)
    g0[0]=symexpr.coeff0
    
    return g,h,g0