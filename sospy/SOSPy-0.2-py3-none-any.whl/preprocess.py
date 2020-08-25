import sympy as sym
import numpy as np
from sympy import *
import math

def preprocess(symexpr,var,interval):
    
#Get the maximum degree of the independent variable    
    maxdeg = 0
    dummy=diff(symexpr,var[0])
    while dummy !=0:
        maxdeg = maxdeg+1
        dummy=diff(dummy,var[0])
#Substitute var
    if interval[1]==math.inf:
        newvar = var+interval[0]
        newsymexpr=symexpr.subs(var[0],newvar)
    elif interval[0]==-math.inf:
        newvar = -var+interval[1]
        newsymexpr=symexpr.subs(var[0],newvar)

    else:
        newvar = (interval[1]-interval[0])/2*(1-var[0])/(1+var[0]) + (interval[1]+interval[0])/2
        newsymexpr = symexpr.subs(var[0],newvar)*(1+var[0])**maxdeg
    
    return newsymexpr