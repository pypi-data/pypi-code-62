#SOSSOLVE2--

import numpy as np
from cvxopt import matrix
from numpy import linalg as LA
import sympy as sym
from sympy import LC,LT,LM, degree,degree_list,expand,nroots,im,prod,sympify,expand
from sympy.physics.quantum import TensorProduct
from sympy import ImmutableMatrix as  Matrix
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from SOSTOOLSPy.getequation import getequation
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from SOSTOOLSPy.addextrasosvar import addextrasosvar
from SOSTOOLSPy.addextrasosvar2 import addextrasosvar2
from SOSTOOLSPy.getequation2 import getequation2
from SOSTOOLSPy.addmultvar import addmultvar


def sossolve2(sos):
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
                At=Attemp
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
                At=Attemp
        else:
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
                
                if sos.interval=='interval':
                    I=1
                    
                    sos.varidx=[len(sos.decvartable) +1] 
                    sos.extravaridx[0]=sos.varidx[sos.varnum+1]
                    if sos.k==0:
                        sos.varidx=[len(sos.decvartable) +1] 
                        sos.extravaridx2[0]=sos.varidx[sos.varnum+1]
                    sos = addextrasosvar2(sos,I)
                    # Processing all variables
                    At=sos.At
                    b=sos.b
                    # Objective function
                    c=np.zeros((At.shape[0],1))
                if sos.interval!='interval':
                    sos.varidx=[len(sos.decvartable) +1] 
                    sos.extravaridx[0]=sos.varidx[sos.varnum+1]
                    if sos.k==0:
                        sos.varidx=[len(sos.decvartable) +1] 
                        sos.extravaridx2[0]=sos.varidx[sos.varnum+1]
                    I=1    
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


        if len(Attemp)==0: #Is is the case of only independent varivables        


                if K.s!=0:
                    c=np.reshape(c, (K.s, K.s))
                else: 
                    K.s=1
                c=matrix(c)


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
    else:
            I=1
            sos.varidx=[len(sos.decvartable) +1] 
            sos.extravaridx[0]=sos.varidx[sos.varnum+1]
            if len(sos.decvartable)>0:
                if sos.type=='ineq':
                    sos=addmultvar(sos,I)
                    At=sos.At
                    b=sos.b
                    c=np.zeros((At.shape[0],1))
                    

                elif sos.type=='eq':
                    At=sos.At
                    b=sos.b
                    c=np.zeros((At.shape[0],1))
                    c=matrix(c)
                    
                                    
    return At,b,c