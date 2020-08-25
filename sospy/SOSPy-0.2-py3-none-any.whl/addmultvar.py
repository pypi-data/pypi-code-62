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
from SOSTOOLSPy.sparsemultipart import sparsemultipart

def addmultvar(sos,I):
    
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
        
        
        Zdummy1=np.apply_along_axis(np.subtract,0, maxdegree, Z)
        Zdummy2=np.apply_along_axis(np.subtract,0,Z.T,mindegree)
        Zdummy2=Zdummy2.T
        ZZdummy=np.concatenate((Zdummy1,Zdummy2),axis=1)
        I=[]
        r=0
        
        for m in range(ZZdummy.shape[0]):
            r=0
            for n in range(ZZdummy.shape[1]):
                if ZZdummy[m][n]<0 and r==0:
                    I=np.concatenate((I,m),axis=None)
                    r=1
                    
        
        IND=np.setdiff1d(np.arange(0,Z.shape[0]), I)
        Z=Z[IND][:]
        
        
        if sos.exprtype=='sparsemultipartite':
            Z2=sos.Z/2
            info2 = sos.exprmultipart #the vectors of independent variables
            sizeinfo2m = len(info2)
            
            vecindex1 = []
            vecindex2 = []
            vecindex=[]
            for indm in range(sizeinfo2m): #for each set of independent variables
                sizeinfo2n=len(info2[indm])
                for indn in range(sizeinfo2n):
                    varcheckindex=[]
                    for m in range(len(sos.symvartable)):
                        if sos.symvartable[m]==info2[indm][indn]:
                            varcheckindex=np.concatenate((varcheckindex,m),axis=None)
                    
                    if len(varcheckindex)!=0:
                        vecindex1=np.concatenate((vecindex1,varcheckindex),axis=None)
                    else:
                        varcheckindex2=[]
                        for m in range(len(sos.varmatsymvartable)):
                            if sos.varmatsymvartable[m]==info2[indm][indn]:
                                varcheckindex2=np.append(varcheckindex2,m)
                        vecindex2=np.concatenate((vecindex2,[len(info2[0])] + varcheckindex2),axis=None)
                        
                        
            vecindex=Matrix([[vecindex1],[vecindex2]]) 
            Z=sparsemultipart(Z,Z2,vecindex)
            
            
             
        
        dimp = sos.b.shape[1] 
       
        
        #Adding slack variables
        
        sos.extravarnum=sos.extravarnum+1
        var=sos.extravarnum
        sos.extravarZ=Z
        
        #Getting the constraint expression
       
        T,ZZ=getconstraint2(Z) 
        sos.extravarZZ=ZZ
        sos.extravarT=T.T
        sos.extravaridx=np.append(sos.extravaridx,sos.extravaridx[var-1]+(Z.shape[0]*dimp)**2) 
        
        #Completing sos.At
       
        sos.At=np.concatenate((sos.At,np.zeros((sos.extravarT.shape[0]*dimp**2,sos.At.shape[1]))),axis=0)
        
        ZZ = np.flipud(ZZ)
        T = np.flipud(T)
        Zcheck=sos.Z
        
        
        
        if dimp==1:
            
            #Ensure correct size
            class  pc: 
                F=[]
                Z=[]
                
            
            pc.Z=sos.extravarZZ
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
           
        else: 
            
            R1,R2,Znew=findcommonZ(Zcheck,ZZ)
            R1=np.fliplr(R1)
            R2 = np.fliplr(R2)
            Znew = np.flipud(Znew)
            
            R1sum=np.sum(R1,axis=0)
            T = np.matmul(R2.T,T)
            ii = 1
            sig_ZZ = ZZ.shape[0]
            sig_Z = Z.shape[0]
            sig_Znew = Znew.shape[0]
            
            Tf = np.zeros((dimp**2*sig_Znew,(dimp*sig_Z)**2))
            Sv = np.zeros((sig_Znew*dimp**2,1))
            
            for j in range(sig_Znew):
                Mt0 = np.zeros((dimp,dimp*sig_Z**2))
                for k in range(sig_Z):
                    Mt0[:,(dimp*sig_Z)*(k):(dimp*sig_Z)*(k+1)]= np.kron(np.eye(dimp),T[j,(sig_Z)*(k):(sig_Z)*(k+1)])
                
                Tf[(j)*dimp**2:(j+1)*dimp**2,:] = np.kron(np.eye(dimp),Mt0)
                
                
                if R1sum[j]==1:
                    Sv[(j)*dimp**2:(j+1)*dimp**2]=np.reshape((sos.b[dimp*(ii-1):dimp*ii,:]).T,(dimp**2,1))
                    if ii<Zcheck.shape[0]:
                        ii = ii+1
                else:
                    
                    sos.At=np.concatenate((sos.At[:,0:(j)*dimp**2],np.concatenate((np.zeros((sos.At.shape[0],dimp**2)),sos.At[:,(j)*dimp**2:sos.At.shape[1]]),axis=1)),axis=1)
                    
                
            lidx=sos.extravaridx[var-1]
            uidx=sos.extravaridx[var]-1
            
            sos.At[lidx-1:uidx,:]=Tf.T
            sos.b=Sv
            
                  
    return sos