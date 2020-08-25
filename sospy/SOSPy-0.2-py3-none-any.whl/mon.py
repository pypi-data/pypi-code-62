import numpy as np
import sympy as sym
from sympy import *
from sympy.polys.monomials import itermonomials
from sympy.polys.orderings import monomial_key

def mon(vartable,maxdeg, mindeg):
    
   
    
    M1=sorted(itermonomials(vartable, mindeg, 0), key=monomial_key('grlex', vartable[::-1] ))
    M2=sorted(itermonomials(vartable, maxdeg, mindeg), key=monomial_key('grlex', vartable[::-1] ))
    
    M1temp=[]
    for i in range(len(M1)):
        if sympify(M1[i]).is_number==False:
            sum_degree=sum(degree_list(M1[i]))
        elif sympify(M1[i]).is_number==True:
            sum_degree=M1[i]
        if sum_degree>=mindeg:
            M1temp=np.append(M1temp,M1[i])
    M1temp=list(M1temp)
    
    M=list(np.append(M1temp,M2))
    M=list(dict.fromkeys(M))
    M=sorted(M, key=monomial_key('grlex', vartable[::-1] ))
    
    
    return M