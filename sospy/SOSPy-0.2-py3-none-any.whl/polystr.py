#Polynomial Structure

import numpy as np
from typing import NamedTuple
import sympy as sym
from sympy import degree_list
from sympy import degree
from sympy import LT
from dataclasses import dataclass
from sympy import sympify

def polystr (polynomial):
    #Given a polynomial we would like to extract some informations of them.
    
    #Extract the coefficients   
    coeff=polynomial.as_coefficients_dict()
    coeff= [ v for v in coeff.values() ]
    coeff=np.asarray(coeff)
    coeff=np.transpose(coeff)
    
    #Extract the number of terms 
    nterms=len(coeff)
    
    #Exctract the independent coefficient- coeff0
    ptemp=polynomial
    coeff0=0
    
    for i in range (nterms-1):
        ptemp=ptemp-LT(ptemp)
        
    
    flag_coeff0=sympify(ptemp).is_number
   
    
    if ptemp!=0 and flag_coeff0==True:
        flag_coeff0=1
    else:
        flag_coeff0=0
    
    if flag_coeff0==1:
        
        coeff0=ptemp
        polynomial=polynomial-ptemp
        
    #Extract the coefficients   
    coeff=polynomial.as_coefficients_dict()
    coeff= [ v for v in coeff.values() ]
    coeff=np.asarray(coeff)
    coeff=np.transpose(coeff)
    
    #Extract the number of terms 
    nterms=len(coeff)    
    
    #Extract the variables
    varname=polynomial.free_symbols
    varname=list(varname)
    varname=np.asarray(varname)
    
    
    #Extract the number of variables
    nvars=len(varname)
    
    cvartable=np.array(varname).astype('str').tolist()
    cvartable=np.asarray(cvartable)
    cvartable=np.sort(cvartable)
    
    # Create the matrix of polynomial degree
    degmat=np.zeros((nterms,nvars))
    ptemp=polynomial
    
    i=0
    k=0
    while(i<=nterms-1 and k<=nvars-1):
        monomial=LT(ptemp,gens=sym.Symbol(cvartable[k]))
        if i<nterms-1:
            ptemp=ptemp-monomial
        if ptemp!=0:
            
            for j in range(nvars):
                degree_var=degree(monomial,gen=sym.Symbol(cvartable[j]))
                if degree==' ' :
                    degmat=[i][j]=0
                else: 
                    degmat[i][j]=degree_var
                    
            i=i+1
        if ptemp==0:
            if k<=nvars-1:
                k=k+1
                ptemp=monomial 
            else:
                ptemp=monomial 
    
    
    if coeff0!=0:
        
        extra_row=np.zeros((1,nvars))
        degmat=np.concatenate((degmat,extra_row), axis=0)
        
      
    #Create maxdeg and mindeg
    max_min=np.zeros((1,nterms))
    for i in range(nterms):
        for j in range(nvars):
            max_min[0][i]+=degmat[i][j]
            
    max_min=np.sort(max_min)
    maxdeg=max_min[0][nterms-1]
    mindeg=max_min[0][0]
    
    #Create decvartable
    decvartable=[]  
    
    #Create varmat
    varmat=[]
    
    #Create vartable and convert in an array
    vartable=polynomial.free_symbols
    
    
    vartable=[]
    for i in range(len(cvartable)):
        vartable=np.append(vartable,sym.Symbol(cvartable[i]))
    
    vartable=list(vartable)
    
    #Create the structure symexpr
    class symexpr:
        polynomial=0
        coefficient=0
        degmat=0 
        varname=0
        nterms=0
        nvars=0
        maxdeg=0 
        mindeg=0 
        coeff0=0
    #Define the valeus in symexpr   
    symexpr=symexpr() 
    symexpr.polynomial=polynomial
    symexpr.coefficient=coeff
    symexpr.nterms=nterms
    symexpr.varname=varname
    symexpr.nvars=nvars
    symexpr.degmat=degmat
    symexpr.maxdeg=maxdeg
    symexpr.mindeg=mindeg
    symexpr.coeff0=coeff0
    
    
       
    return symexpr, decvartable, varmat, vartable