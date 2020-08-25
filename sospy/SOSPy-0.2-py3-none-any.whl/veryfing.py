import numpy as np
import sys
import mosek
from   mosek.fusion import *
from numpy import linalg as LA
import sympy as sym
from sympy import LC,LT,LM, degree,degree_list,expand,nroots,im,prod,sympify,expand
from sympy.physics.quantum import TensorProduct
from sympy.matrices import eye, zeros, ones, diag, Transpose
from SOSTOOLSPy.getequation import getequation
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from SOSTOOLSPy.addextrasosvar import addextrasosvar
from SOSTOOLSPy.getequation2 import getequation2
from SOSTOOLSPy.addmultvar import addmultvar

def veryfing(sos,options):
   
    if len(sos.vartable)==1: #One only variable
        unfeasible=0
        if sos.type=='eq':

            polynomial=sos.polynomial

            for i in range(len(sos.decvartable)):
                polynomial=polynomial-expand(sos.decvartable[i]*polynomial.coeff(sos.decvartable[i]))
            if polynomial==0 or degree(polynomial) == 0:
                poly=polynomial
                Attemp=np.zeros((len(sos.decvartable),len(sos.Z)))
                for j in range(len(sos.decvartable)):
                    polynomial=sos.polynomial.coeff(sos.decvartable[j])

                    if polynomial!=0 and degree(polynomial)!=0:

                        symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                        bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)

                        indexAt=[]
                        idexc=np.isin(sos.Z,Zg)
                        for m in range(idexc.shape[0]):
                            if idexc[m]==True:
                                indexAt=np.concatenate((indexAt, m), axis=None)

                        #Creating the vector Attemp
                        for l in range(len(indexAt)):
                            Attemp[j][int(indexAt[l])]=-bg[l]


                    else:
                        bg=polynomial
                        Attemp[j][len(sos.Z)-1]=-bg


                # Objective function
                c=np.zeros((Attemp.shape[0],1))
                b=np.zeros((Attemp.shape[1],1))
                b[Attemp.shape[1]-1][0]=poly

            else: 

                poly=polynomial
                Attemp=np.zeros((len(sos.decvartable),len(sos.Z)))
                for j in range(len(sos.decvartable)):
                    polynomial=sos.polynomial.coeff(sos.decvartable[j])

                    if polynomial!=0 and degree(polynomial)!=0:

                        symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                        bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)

                        indexAt=[]
                        idexc=np.isin(sos.Z,Zg)
                        for m in range(idexc.shape[0]):
                            if idexc[m]==True:
                                indexAt=np.concatenate((indexAt, m), axis=None)

                        #Creating the vector Attemp
                        for l in range(len(indexAt)):
                            Attemp[j][int(indexAt[l])]=-bg[l]


                    else:
                        bg=polynomial
                        Attemp[j][len(sos.Z)-1]=-bg

                c=np.zeros((Attemp.shape[0],1))
                b=np.zeros((Attemp.shape[1],1))
                for p in range(b.shape[0]):
                    b[p][0]=sos.b[p]

        else:
            if sos.nconstraint==1:

                #As we have inequalities constraints in sos
                I=1

                Attemp=sos.At
                nzeros=0
                if sos.coeff0==0:
                    for l in range(sos.At.shape[0]):
                        if sos.At[l][0]==0:
                            nzeros=nzeros+1
                    if nzeros==sos.At.shape[0]:
                        sos.At=np.delete(sos.At, 0, 1)
                        Attemp=sos.At
                        sos.At=[]


                polynomial=sos.polynomial
                for m in range(len(sos.decvartable)):
                    polynomial=polynomial-expand(sos.decvartable[m]*polynomial.coeff(sos.decvartable[m]))



                odd=0
                if int(sos.Z[0])%2!=0:
                    sos.Z[0]=sos.Z[0]-1
                    odd=1



                #it is necessary to convert this canonical optimization problem to the standard form.
                sos = addextrasosvar(sos,I)


                if odd==1:
                    A=np.zeros((sos.At.shape[0],1))
                    sos.At=np.concatenate((sos.At, A), axis=1)
                    sos.b=np.append(sos.b,[0])

                if len(Attemp)!=0 and sos.At.shape[1]!=Attemp.shape[1]:
                    difcol=abs(Attemp.shape[1]-sos.At.shape[1])
                    Ad=np.zeros((sos.At.shape[0],int(difcol)))
                    sos.At=np.concatenate((Ad,sos.At), axis=1)
                    #Constructing b again
                    b=np.zeros((1,sos.At.shape[1]))
                    if polynomial!=0 and degree(polynomial)!=0:
                        symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                        bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                    elif polynomial!=0 and degree(polynomial)==0:
                        bg=[polynomial]
                        Zg=[1]
                    else:
                        bg=[polynomial]
                        Zg=[1]
                    for n in range(len(bg)):
                        b[0][int(Zg[n])-1]=bg[n]
                    sos.b=b[0]
                # Processing all variables
                At=sos.At
                b=sos.b



                if len(Attemp)!=0:
                    At=np.concatenate((Attemp, At), axis=0)

                class K:
                    s=[]
                    f=0   
                K.s=(sos.extravaridx[1]-sos.extravaridx[0])**0.5
                K.s=int(np.ceil(K.s))


                K.s=int(np.sqrt(sos.At.shape[0]))

                # Objective function
                c=np.zeros((At.shape[0],1))


                #Calling the solver

        if options=='mosek': #Solving the optimization problem
            #1st case
            if sos.nconstraint==1 and len(Attemp)==0: #Is is the case of only independent varivables        

                if K.s!=0:
                    c=np.reshape(c, (K.s, K.s))
                else: 
                    K.s=1
                c=Matrix.dense(c)


                if odd==1:
                    symexprg,decvartableg,varmatg,vartableg=polystr(sos.polynomial)
                    bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                    b=np.zeros((int(Zg[0][0])+1,1))
                    for s in range(len(bg)):
                        b[int(Zg[s][0])][0]=bg[s]



                #Constructing b again
                b=np.zeros((1,sos.At.shape[1]))
                symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                bg=bg[::-1]
                idexfind=np.isin(sos.Z,Zg)
                idexfindc=[]
                for o in range(len(idexfind)):
                    if idexfind[o]==True:
                        idexfindc= np.concatenate((idexfindc, o), axis=None)
                for p in range(len(idexfindc)):
                    b[0][int(idexfindc[p])]=bg[p]

                b=b[0]
                
                flag_positivity=0
                #Solving the problem
                with Model("SDP1") as M1:

                    X=M1.variable('X',Domain.inPSDCone(K.s))
                    M1.objective(ObjectiveSense.Minimize, Expr.dot(c,X))
                    M1.constraint(Expr.sub(Expr.mul(At.T,X.reshape(K.s**2,1)), b.T), Domain.equalsTo(0.0))
                    M1.solve()
                    info=M1.getProblemStatus()
                   
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        x=[]
                    if info==ProblemStatus.Unknown or info==ProblemStatus.PrimalInfeasible or info==ProblemStatus.DualInfeasible :
                        x=[]
                        flag_positivity=-1
                    else:      
                        x=np.asarray(X.level())
                    
                
                if x==[] and flag_positivity==0:
                    flag_positivity+=1
                    info='Unfeasible Problem'
                elif x==[] and flag_positivity==-1:
                    flag_positivity=-1
                    info='Consider the first problem'
                else:
                    x=np.reshape(x,(At.shape[0],1))
                    RR=np.eye(len(x))
                    RRx=np.matmul(RR,x)
                    
                    Q=np.reshape(RRx, (int(np.sqrt(len(RRx))), int(np.sqrt(len(RRx)))))
                    w, v = LA.eig(Q)


                    numzeig=0
                    nmax=np.amax(w)

                    for i in range(len(w)):
                        if w[i]/nmax<10**-3 or abs(w[i])<10**-3:
                            if w[i]<0:
                                w[i]=-0
                            else:
                                w[i]=0
                        if w[i]<0 and abs(w[i])>1*10**-1:##10e-1 or 10e-6
                            flag_positivity+=1
                            info='Unfeasible Problem'
                        if w[i]==0:
                            numzeig=numzeig+1

                    if numzeig==len(w):
                        flag_positivity+=1
                        info='Unfeasible Problem'


                    Z=np.eye(len(sos.extravarZ))
                    Zmon=zeros(int(Zg[0][0]/2 + 1),1)


                    for i in range(len(Zmon)):
                        Zmon[i]=sos.vartable[0]**int(i)

                    if Zg[len(Zg)-1]!=0:
                        Zmontemp=zeros(Zmon.shape[0]-1,1)
                        for l in range(Zmontemp.shape[0]):
                            Zmontemp[l]=Zmon[l+1]
                        Zmon=Zmontemp
                    if (len(Q)==1):
                        Zmon=sos.vartable[0]**int(sos.Z[0]/2)

                    num_zero=0
                    for i in range(Q.shape[0]):
                        for j in range(Q.shape[1]):
                            if Q[i][j]==0:
                                num_zero+=1

                    if num_zero==(Q.shape[0]*Q.shape[1]):
                        flag_positivity+=1

                    

            
            
    #2nd case                     
    else:
        if sos.nconstraint==1:
            I=1
            sos.varidx=[len(sos.decvartable) +1] 
            sos.extravaridx[0]=sos.varidx[sos.varnum+1]
            if sos.flag_findsos==1:
                
                sos=addmultvar(sos,I)
                At=sos.At
                b=sos.b
                c=np.zeros((At.shape[0],1))
                
               
                class K:
                    s=[]
                    f=0   
               
                K.s=int(np.sqrt(sos.At.shape[0]))
                if K.s!=0:
                    c=np.reshape(c, (K.s, K.s))
                else: 
                    K.s=1
                c=Matrix.dense(c)
                
                flag_positivity=0
                #Solving the problem
                with Model("SDP7") as M7:

                    X=M7.variable('X',Domain.inPSDCone(K.s))
                    M7.objective(ObjectiveSense.Minimize, Expr.dot(c,X))
                    M7.constraint(Expr.sub(Expr.mul(At.T,X.reshape(K.s**2,1)), b), Domain.equalsTo(0.0))
                    M7.solve()
                    info=M7.getProblemStatus()
                    
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        x=[]
                    if info==ProblemStatus.Unknown or info==ProblemStatus.PrimalInfeasible or info==ProblemStatus.DualInfeasible :
                        x=[]
                        flag_positivity=-1
                    else:      
                        x=np.asarray(X.level())
                    
                
                if x==[] and flag_positivity==0:
                    flag_positivity+=1
                    info='Unfeasible Problem'
                elif x==[] and flag_positivity==-1:
                    flag_positivity=-1
                    info='Consider the first problem'
                else:    
                    x=np.reshape(x,(At.shape[0],1))
                    RR=np.eye(len(x))
                    RRx=np.matmul(RR,x)
                    
                    Q=np.reshape(RRx, (int(np.sqrt(len(RRx))), int(np.sqrt(len(RRx)))))
                    w, v = LA.eig(Q)

                    flag_positivity=0
                    numzeig=0
                    nmax=np.amax(w)

                    for i in range(len(w)):
                        if w[i]/nmax<10**-3 or abs(w[i])<10**-3:
                            if w[i]<0:
                                w[i]=-0
                            else:
                                w[i]=0
                        if w[i]<0 and abs(w[i])>1*10**-1:##10e-1 or 10e-6
                            flag_positivity+=1
                            info='Unfeasible Problem'
                        if w[i]==0:
                            numzeig=numzeig+1

                    if numzeig==len(w):
                        flag_positivity+=1
                        info='Unfeasible Problem'


                    if len(Q)!=0:
                        Zmontemp=TensorProduct(sos.vartable,ones(sos.extravarZ.shape[0],1))**sos.extravarZ
                        Zmon=zeros(Zmontemp.shape[0],1)
                        for i in range(Zmontemp.shape[0]):
                            Zmon[i]=prod(Zmontemp[i][:])

                    else:
                        flag_positivity+=1
                        info='Unfeasible Problem'

                    
                
      
    
    return flag_positivity