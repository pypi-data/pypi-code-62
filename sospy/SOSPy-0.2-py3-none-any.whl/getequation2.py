import numpy as np
from typing import NamedTuple
import sympy as sym
from sympy import LT,LM,degree,degree_list
from SOSTOOLSPy.collect import collect 
from dataclasses import dataclass
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from scipy.sparse import csr_matrix
from SOSTOOLSPy.ismember import ismember
from SOSTOOLSPy.sortNoRepeat import sortNoRepeat
from SOSTOOLSPy.max_kron import max_kron
from SOSTOOLSPy.polystr import polystr

def getequation2(symexpr,decvartable,varmat,vartable):
    
     # Handle Polynomial Objects including the Matrix Case

    decvarnum=len(decvartable)
    vartable=np.concatenate((vartable,varmat))
    cvartable=np.array(vartable).astype('str').tolist()
    cvartable=np.asarray(cvartable)
    cvartable=np.sort(cvartable)
    dimp=1 # It could be changed 
    
    #Collect symexpr = g(c)*h(x) + g0 where x are the vars in vartable,
    #c are the decision variables, and h(x) is a vector of monoms.
    #in the actual polynomial vars.  Use this to find unique
    #monomials in the polynomial variables.
   
    g,h,g0=collect(symexpr)
    
    #Then the polynomial expression was divised in three terms, such that p=g*h+g0
    h0=zeros(1,1)
    h0[0]=1
    if g0[0] != 0:
        g=g.col_join(g0)
        h=h.col_join(h0)
        
    #Define the numbers of mononials and variables in p
    nmon=symexpr.nterms
    nvar=symexpr.nvars
    
    #Reorder the monomials matrix with variables in the order listed in cvartable and sorted monomials

    #Create the matrix Z, which will receive the monomials of the expression
    Z=zeros(nmon,nvar)
    Z=symexpr.degmat
    #Creating the matrix Z in the multivariable case
    if len(vartable)!=1:
        polynomial=symexpr.polynomial+symexpr.coeff0
        for i in range(len(decvartable)):
            polynomial=polynomial.subs(decvartable[i],1)
        symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
        if symexprg.coeff0!=0:
            nterms=symexprg.nterms+1
        else:
            nterms=symexprg.nterms
        Z=np.zeros((nterms,len(vartable)))
        for k in range(symexprg.nterms):
            mon=LT(polynomial)
            for j in range(len(vartable)):
                deg=degree(mon,gen=vartable[j])
                Z[k][j]=deg
            polynomial=polynomial-LT(polynomial)


    #The vector b will receive the coefficients of the the symbolic expression

    b=g.T

    
    
    return b,Z