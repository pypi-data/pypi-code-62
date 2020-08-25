import numpy as np
import sympy as sym
from sympy import degree_list,degree,LT,LM,LC,sympify
from sympy import matrix2numpy
from sympy.core.compatibility import as_int
from SOSTOOLSPy.getequation import getequation
from sympy import ImmutableMatrix as  Matrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from scipy.sparse import csr_matrix
from scipy import sparse
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from sympy import poly
from sympy import factor
from SOSTOOLSPy.monomials2 import monomials2
from  SOSTOOLSPy.getconstraint2 import getconstraint2
from SOSTOOLSPy.findcommonZ import findcommonZ

def addextrasosvar2(sos,I):
    sos.At=np.flip(sos.At, axis=1)
    for i in range(I):
        
        
        numstates=sos.Z.shape[1]

        # Creating extra variables
        maxdeg = np.amax(sos.Z.sum(axis=1))
        mindeg = np.amin(sos.Z.sum(axis=1))
        floor_deg=np.floor(mindeg/2) 
        ceil_deg=np.ceil(maxdeg/2)
        d=np.arange(floor_deg,ceil_deg+1)
        
        
        
        #Creating the candidate monomials
        
        
        Z=monomials2(numstates,d) ## Work here for the preprocessing of this toolbox 
        
        
        #Discarding unnecessary monomials
        
        
        maxdegree = np.max(sos.Z, axis=0)/2 
        mindegree = np.min(sos.Z, axis=0)/2 
        
        j=0
        
        while j+1<=Z.shape[0]:
            Zdummy1 = maxdegree-Z[j][:]
            Zdummy2 = Z[j][:]-mindegree
            Zdummy=[Zdummy1,Zdummy2]
            idx=[]
            for i in range(len(Zdummy)):
                if Zdummy[i][0]<0:
                    idx=np.concatenate((idx,i),axis=None)
            if len(idx)!=0:
                Z = np.array([[Z[0:j,:]], [Z[j:][:]]])
            else:
                j = j+1
            
        #Adding slack variables
        for k in range(2):
            sos.extravarnum=sos.extravarnum+1
            var=sos.extravarnum
            sos.extravarZ=Z
            
            #TEST
            sos.extravarnum2=sos.extravarnum2+1
            var2=sos.extravarnum2
            #Getting the constraint expression


            T,ZZ=getconstraint2(Z) 
            sos.extravarZZ=ZZ
            sos.extravarT=T.T
            sos.extravaridx=np.append(sos.extravaridx,sos.extravaridx[var-1]+(Z.shape[0])**2)  
            #TEST
            sos.extravaridx2=np.append(sos.extravaridx2,sos.extravaridx2[var2-1]+(Z.shape[0])**2)  

            #Completing sos.At

            sos.At=np.concatenate((sos.At,np.zeros((sos.extravarT.shape[0],sos.At.shape[1]))),axis=0)

         

            #Modifying expression
            degoffset = k*np.ones((sos.extravarZZ.shape[0],1))
            #Ensure correct size
            class  pc: 
                F=[]
                Z=[]
            
            
            
            
            pc.Z=sos.extravarZZ+degoffset
            pc.F=-np.eye(pc.Z.shape[0], dtype=int)
            
            R1,R2,newZ=findcommonZ(sos.Z,pc.Z)
            
            if len(sos.At)==0:
                sos.At=np.zeros((sos.At.shape[0],R1.shape[0]))
            
            sos.At=np.matmul(sos.At,R1)
            lidx=sos.extravaridx[var-1]
            uidx=sos.extravaridx[var]-1
            sos.At[lidx-1:uidx][:]=sos.At[lidx-1:uidx][:]-np.matmul(np.matmul(sos.extravarT,pc.F),R2)
            sos.b=np.matmul(R1.T,sos.b)
            sos.Z=newZ
            
            findidx=[]
            for j in range(Z.shape[0]):
                if Z[j]<maxdegree:
                    findidx=np.concatenate((findidx,j),axis=None)
            Z=Z[findidx.astype(int)]       
            
    return sos