#Find the elements in Z1 that are in the convex hull of Z2, where Z2 is bipartite


import numpy as np
import sympy as sym
from sympy import *
from SOSTOOLSPy.inconvhull import inconvhull

def sparsemultipart(Z1,Z2,info):
    
    sum_Z2=np.sum(Z2,axis=0)
    Y=[]
    I=[]
    for i in range(len(sum_Z2)):
        if sum_Z2[i]==0:
            I=np.concatenate((I,i),axis=None)
            Y=np.concatenate((Y,sum_Z2[i]),axis=None)
    sizeinf=len(info) 
    
    if sizeinf==1:
        print('Error in sparsemultipart option - at least two sets are required')
        Z=[]
    else:
        var_holder = {}
        for i in range(sizeinf):
            var_holder['Z3_' + str(i)]=[]
        locals().update(var_holder)
        for i in range(sizeinf):
            info_i=np.asarray(info[i])
            var_holder['Z3_' + str(i)]=inconvhull(Z1[:,info_i.astype(int)],Z2[:,info_i.astype(int)]) 
            
    for i in range(sizeinf-1):
        var_holder['Z3_' + str(i+1)]=np.concatenate((np.matlib.repmat(var_holder['Z3_' + str(i)],var_holder['Z3_' + str(i+1)].shape[0],1),np.kron(var_holder['Z3_' + str(i+1)],np.ones((var_holder['Z3_' + str(i)].shape[0],1)))),axis=1)
    
    Z3=var_holder['Z3_' + str(sizeinf-1)]
    Z=np.zeros((Z3.shape[0],Z2.shape[1]))
    lgth = 0
    
    
    for i in range(sizeinf):
        
        Z[:,(np.asarray(info[i])).astype(int)]= Z3[:,(lgth):(lgth+len(info[i]))]
        lgth = len(info[i])+lgth
    
    
    
    if len(I)!=0:   
        Z[:,(np.asarray(I)).astype(int)] = np.zeros((Z.shape[0],(np.asarray(I)).shape[1]))
    
    
      
    return Z