import numpy as np
import sympy as sym
from sympy import *
from numpy import *
from scipy.spatial import ConvexHull
from scipy.linalg import null_space
from sympy import  Matrix,nsimplify,expand

def useconvhulln(Z2):
    
    
    convh=ConvexHull(Z2).simplices 
    facets = convh.shape[0]
    nZ1,nZ2 = Z2.shape
    
   
    #Form the hyperplanes
    #A hyperplane of the form [x1 ... xn -ones][A';b'] = 0
    #[A';b'] is in the nullspace of the matrix [x1,...,xn -ones].
    #Ignore it if it has dimension greater than 1
    #Normalise if possible.
    
    coeff=np.zeros((facets-1,facets))
    
    cold=np.zeros((facets,1))
    for i in range(facets):
        vert=np.concatenate((Z2[convh[i,:].astype(int),:],-np.ones((nZ2,1))),axis=1)
        vert=np.asarray(vert)
        nullvert = (nsimplify(Matrix(vert), rational=True).nullspace())[0]
        if nullvert.shape[1]==1:
            if nullvert[nullvert.shape[0]-1] !=0:
                nullvert = nullvert/(nullvert[nullvert.shape[0]-1])
        nullvert=np.asarray(nullvert)         
        
        
        for j in range(coeff.shape[0]):
            coeff[j][i]=nullvert[j]
            
        cold[i][0]=nullvert[nullvert.shape[0]-1]
    
    coeff=coeff.T
   
    
    #Condition the matrix a bit
    coeffcold=np.concatenate((coeff,cold),axis=1)
    
    #Discard same hyperplanes (due to convhulln result)
    coeff2cold,Ix,Iy  = np.unique(coeffcold, axis=0, return_index=True, return_inverse=True)
    
    #Remove a possible zero row
    
    sum_yind=np.sum(coeff2cold,axis=1)
    yind=[]
    for i in range(len(sum_yind)):
        if sum_yind[i]==0:
            yind=np.concatenate((yind,i),axis=None)
            
    if len(yind)!=0:
        for i in range(len(yind)):
            Ix.pop(yind[i])
    
    coeff2=coeff[Ix.astype(int),:]
    convhnew=convh[Ix.astype(int),:]
    cnew = cold[Ix.astype(int)]
    facetsnew=convhnew.shape[0]
    
    #Make inequalities out of them by testing a point not on the hyperplane
    #Notation: convex hull is now Ax-b<=0    
    
    for fac in range(facetsnew):
        for ind in range(nZ1):
            matr=[]
            matrtemp=convhnew[fac,:] - ind*np.ones((1,nZ2))
            
            for i in range(len(matrtemp[0])):
                if matrtemp[0][i]==0:
                    matr=np.concatenate((matr,i),axis=None)
                    
            tests = matmul(coeff2[fac,:],(Z2[ind,:].T))-cnew[fac]
            
            if len(matr)==0 and abs(tests)>1e-8:
                break 
                
        if tests>0:
            coeff2[fac,:]=-coeff2[fac,:]
            cnew[fac]=-cnew[fac]
            
            
    
    A=coeff2
    B=cnew
    
    
    return A,B