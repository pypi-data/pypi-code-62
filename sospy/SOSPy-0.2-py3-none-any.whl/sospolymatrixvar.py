import sympy as sym
import numpy as np
from sympy import *
from SOSTOOLSPy.sospolyvar import sospolyvar

def sospolymatrixvar(prog,monomials,dim,option):
    
    M=-ones(dim[0],dim[1])
    if option!='symmetric' and option!='diagonal':
        for i in range(dim[0]):
            for j in range(dim[1]):
                prog,M[i,j]=sospolyvar(prog,monomials)
    elif option=='symmetric' : #Symmetric Matrix Case
        for i in range(dim[0]):
            for j in range(dim[1]):
                if i<=j:
                    prog,M[i,j]=sospolyvar(prog,monomials)
                
        for i in range(dim[0]):
            for j in range(dim[1]):
                if M[i,j]==-1:
                    M[i,j]=M[j,i]
                
    elif option=='diagonal' : #Diagonal Matrix Case
        for i in range(dim[0]):
            for j in range(dim[1]):
                if i==j:
                    prog,M[i,j]=sospolyvar(prog,monomials)
                if M[i,j]==-1:
                    M[i,j]=0
    return prog, M


