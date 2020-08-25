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
from SOSTOOLSPy.monomials import monomials
from  SOSTOOLSPy.getconstraint import getconstraint
from SOSTOOLSPy.findcommonZ import findcommonZ

def addextrasosvar(sos,I):
    
    
    for i in range(I):
        
        numstates=sos.Z.shape[1]

        # Creating extra variables
        maxdeg = np.amax(sos.Z.sum(axis=1))
        mindeg = np.amin(sos.Z.sum(axis=1))
        floor_deg=np.floor(mindeg/2) 
        ceil_deg=np.ceil(maxdeg/2)
        d=np.arange(floor_deg,ceil_deg+1)
        
        #Creating the candidate monomials
  
        Z=monomials(numstates,d)
        
        
        #Discarding unnecessary monomials
        
        maxdegree = np.max(sos.Z, axis=0)/2 #It is necessary to convert this to a sparse matrix
        mindegree = np.min(sos.Z, axis=0)/2 #It is necessary to convert this to a sparse matrix
        
        Zdummy1=np.apply_along_axis(np.subtract,0, maxdegree, Z)
        Zdummy2=np.apply_along_axis(np.subtract,0,Z,mindegree)
        
        ZZdummy=np.concatenate((Zdummy1,Zdummy2),axis=0)
        ZZdummy=sparse.csr_matrix(ZZdummy)
        l=ZZdummy.shape[0]
        g=ZZdummy.shape[1]
        I=[]
        r=0
       
        
        IND=np.setdiff1d(np.arange(0,Z.shape[0]), I)
        Z=Z[IND][:]
      
       
        
        Z=np.zeros((1,int(sos.Z[0][0]/2)+1))

        for i in range (int(sos.Z[0][0]/2+1)):
             Z[0][i]=i
                
        if sos.coeff0==0 and len(sos.At)==0:
            Z=np.delete(Z[0],0,0)        
         
        if sos.matrixtype==1:
            dimp = sos.b.shape[1]
            
        else:
            dimp = sos.b.shape[0]
        
   
        
        #Adding slack variables
        
        #For this toolbox we are working with only expression per time, then the number of expressions here is 1
        
        
        sos.extravarnum=sos.extravarnum+1
        var=sos.extravarnum
        sos.extravarZ=Z
        
        
        if sos.flag_interval!=0:
            sos.extravarnum2=sos.extravarnum2 + 1
            var2=sos.extravarnum2
        
      
        #Getting the constraint expression
        
        if len(sos.At)==0:
            if sos.coeff0!=0:
                T,ZZ=getconstraint(Z[0]) #Test
            else:
                T,ZZ=getconstraint(Z)        
        else:
            T,ZZ=getconstraint(Z[0])
          
       
        sos.extravarZZ=ZZ
        sos.extravarT=T.T
        if sos.matrixtype==1:
            if sos.coeff0!=0:
                Z=Z[0]
            
            sos.extravaridx=np.append(sos.extravaridx,sos.extravaridx[var-1]+(len(Z)*dimp)**2)
        else:
            sos.extravaridx=np.append(sos.extravaridx,sos.extravaridx[var-1]+(Z.shape[0]*dimp)**2)
        
        
        if sos.flag_interval!=0:
            
            sos.extravaridx2=np.append(sos.extravaridx2,sos.extravaridx2[var2-1]+(Z[0].shape[0]*dimp)**2)  
        
        
        
            
        ZZ = np.flipud(ZZ)
        T = np.flipud(T)
        
        if sos.matrixtype==1:
            #Completing sos.At
            
            sos.At=np.concatenate((sos.At,np.zeros((sos.extravarT.shape[0]*dimp**2,sos.At.shape[1]))),axis=0)
            
            ZZtemp=np.zeros((len(ZZ),1))
            for i in range(len(ZZ)):
                ZZtemp[i][0]=ZZ[i]    
            ZZ=ZZtemp
            
        Zcheck=sos.Z
        
        if dimp==1:
            
            #Ensure correct size
            class  pc: 
                F=[]
                Z=[]
                
             
            
            if sos.extravarZZ[len(sos.extravarZZ)-1]!=sos.Z[0][0]:
                for i in range(int(sos.Z[0][0]-sos.extravarZZ[len(sos.extravarZZ)-1])):
                    sos.extravarZZ=np.append(sos.extravarZZ,sos.extravarZZ[len(sos.extravarZZ)-1]+1)

            pc.Z=sos.extravarZZ
            pc.F=-np.eye(pc.Z.shape[0], dtype=int)

            newZ=pc.Z
          
            R2=np.eye(pc.Z.shape[0], dtype=int)
         
            
            R1=np.zeros((sos.Z.shape[0],pc.Z.shape[0]))
            
            
            for j in range(sos.extravarnum):
                sos.At=np.zeros((T.shape[1]*dimp**2,sos.Z.shape[0]))
            
            
            flag_zero=0
            for j in range(len(sos.Z)):
                if sos.Z[j][0]==0:
                    flag_zero=1
            if flag_zero==0:
                for j in range(len(sos.Z)):
                    sos.Z[j][0]=sos.Z[j][0]-2
                        
            flag_odd=0 
            if flag_zero==0:
                for j in range(len(sos.Z)):
                    if (sos.Z[j][0]% 2)!=0:
                        flag_odd=1   
                if flag_odd==1:
                    for j in range(len(sos.Z)):
                        sos.Z[j][0]=sos.Z[j][0]-1
                        
            if len(sos.Z)==1:
                sos.Z[0]=0
            
            
            for k in range(sos.Z.shape[0]):
                R1[k][int(sos.Z[k])]=1
            
            var=0
            sos.At=np.matmul(sos.At,R1)
            lidx = sos.extravaridx[var]
            uidx = sos.extravaridx[var+1]
            sos.At=sos.At-np.matmul(sos.extravarT,np.matmul(pc.F,R2))
            sos.b=matrix2numpy(sos.b)
            btemp=np.zeros((sos.b.shape))
            for i in range(sos.b.shape[1]):
                btemp[0][i]=sos.b[0][i]
            sos.b=btemp
            sos.b=np.matmul(R1.T,sos.b.T)
            sos.Z = newZ 
            
            
            
        else:
            
            R1,R2,Znew=findcommonZ(Zcheck,ZZ)
            R1=np.fliplr(R1)
            R2 = np.fliplr(R2)
            Znew = np.flipud(Znew)
          
            
            R1sum=np.sum(R1,axis=0)
            
            T = np.matmul(R2.T,T)
            ii = 1
            sig_ZZ = ZZ.shape[0]
            sig_Z =len(Z)
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