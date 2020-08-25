#Find a sum of squares decomposition of a given matrix polynomial.
import numpy as np
import sympy as sym 
from numpy import *
from sympy import *
from SOSTOOLSPy.getequation import getequation
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.sossolve import sossolve
from SOSTOOLSPy.getequationmc import getequationmc
from scipy.linalg import sqrtm
from sympy.physics.quantum import TensorProduct


def findsos(p,flag,options):
    
    if flag != 'rational': 
        options='mosek' #options=flag
        flag = 'abcdefgh'
    else: 
        options='mosek'
        flag = 'abcdefgh'
    
    
    if np.asarray(p).shape==():
        
        symexpr,decvartable,varmat,vartable=polystr(p)
        At,b,Z,sos=getequation(symexpr,decvartable,varmat,vartable)
        sos.polynomial=p
        sos.flag_findsos=1
        sol=sossolve(sos,options)

        if len(sol.Q)==0:
            print('No sum of squares decomposition is found')
            decomp=[]
        else:
            print('Sum of squares decomposition found')
            L=sqrtm(sol.Q)
            decomp= L*(TensorProduct(eye(1),sol.Zmon))
        
    else: 
        decvartabletemp=[]
        vartabletemp=[]
        for i in range(p.shape[0]):
            for j in range(p.shape[1]):
                symexpr,decvartable,varmat,vartable=polystr(p[i,j])
                
                decvartabletemp=np.concatenate((decvartabletemp,decvartable),axis=None)
                vartabletemp=np.concatenate((vartabletemp,vartable),axis=None)
        
        vartable=list((Matrix(np.unique(np.array(vartabletemp).astype('str').tolist()))))
        decvartable=list((Matrix(np.unique(np.array(decvartabletemp).astype('str').tolist()))))
        
        At,b,Z,sos=getequationmc(p,decvartable,vartable)
        
        sos.matrixtype=1
        sos.polynomial=p
        sos.flag_findsos=1
        sol=sossolve(sos,options)
        if len(sol.Q)==0:
            print('No sum of squares decomposition is found')
            decomp=[]
        else:
            print('Sum of squares decomposition found')
            L=sqrtm(sol.Q)
            decomp= L*(TensorProduct(eye(p.shape[0]),sol.Zmon))
        
        
    
    
    
    return sol.Q,sol.Zmon,decomp


