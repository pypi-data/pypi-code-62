#SOSSOLVE --- Solve a sum of squares program.
#SOSP = sossolve(SOSP) SOSP is the SOS program to be solved.


import numpy as np
import sys
import mosek
from   mosek.fusion import *
from numpy import linalg as LA
import sympy as sym
from sympy import LC,LT,LM, degree,degree_list,expand,nroots,im,prod,sympify,expand
from sympy.physics.quantum import TensorProduct
from sympy.matrices import  eye, zeros, ones, diag, Transpose
from SOSTOOLSPy.getequation import getequation
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.max_kron import max_kron 
from SOSTOOLSPy.collect import collect
from SOSTOOLSPy.addextrasosvar import addextrasosvar
from SOSTOOLSPy.getequation2 import getequation2
from SOSTOOLSPy.addmultvar import addmultvar
from SOSTOOLSPy.veryfing import veryfing

def sossolve(sos,options):
    
    sostemp=sos
    if len(sos.vartable)==1: #One only variable
        unfeasible=0
        if sos.type=='eq':

            polynomial=sos.polynomial

            for i in range(len(sos.decvartable)):
                polynomial=polynomial-expand(sos.decvartable[i]*polynomial.coeff(sos.decvartable[i]))#Using expand here
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
                
                if sos.matrixtype==0:
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
                        polynomial=polynomial-expand(sos.decvartable[m]*polynomial.coeff(sos.decvartable[m]))#Using expand here



                    odd=0
                    if int(sos.Z[0])%2!=0:
                        sos.Z[0]=sos.Z[0]-1
                        odd=1



                #it is necessary to convert this canonical optimization problem to the standard form.
                
                if sos.matrixtype==1:
                    Attemp=sos.At
                    sos=addextrasosvar(sostemp,I)
                    At=sos.At
                    b=sos.b
                    b=b.T
                    
                else:
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

                if sos.matrixtype==0:

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

                #Solving the problem
                with Model("SDP1") as M1:
                    
                    X=M1.variable('X',Domain.inPSDCone(K.s))
                    M1.objective(ObjectiveSense.Minimize, Expr.dot(c,X))
                    M1.constraint(Expr.sub(Expr.mul(At.T,X.reshape(K.s**2,1)), b.T), Domain.equalsTo(0.0))
                    M1.setLogHandler(sys.stdout)
                    M1.solve()
                    info=M1.getProblemStatus()
              
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        
                        x=[]
                    else:      
                        x=np.asarray(X.level())

 
                
                if x==[]:
                    info='Unfeasible Problem'
                    Q=[]
                    Zmon=[]
                    ptemp=[]
                    
                else:
                    x=np.reshape(x,(At.shape[0],1))
                    RR=np.eye(len(x))
                    RRx=np.matmul(RR,x)
                    np.set_printoptions(precision=4)
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


                    if sos.matrixtype==0:
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
                    else:
                        
                        
                        Zmontemp=(TensorProduct(np.asarray(sos.vartable),ones(len(sos.extravarZ),1))**sos.extravarZ)[0]
                        Zmon=zeros(len(Zmontemp),1)
                        for i in range(Zmon.shape[0]):
                            Zmon[i]=Zmontemp[i]

                    num_zero=0
                    for i in range(Q.shape[0]):
                        for j in range(Q.shape[1]):
                            if Q[i][j]==0:
                                num_zero+=1

                    if num_zero==(Q.shape[0]*Q.shape[1]):
                        flag_positivity=1

                    if flag_positivity>0:
                        Q=[]
                    ptemp=sos.polynomial    

            elif sos.nconstraint==1 and len(Attemp)!=0: # Case with decision variables


                #2nd case
                
                if sos.type=='ineq':

                    K.f=len(Attemp)
                    
                    if len(sos.obj)!=0:
                        for j in range(len(sos.obj)):
                            for i in range(len(sos.decvartable2)):
                                if sos.obj[j].coeff(sos.decvartable2[i])!=0:
                                    c[i][0]=sos.obj[j].coeff(sos.decvartable2[i])
                  
                    
                    
                    
                    c1=c[0:K.f]
                    c2=c[K.f:len(c)]
                    c2=np.reshape(c2, (K.s, K.s))  
                    c1=Matrix.dense(c1)
                    c2=Matrix.dense(c2)
                    A1=Attemp
                    
                    with Model("SDP2") as M2:
                        X1=M2.variable([K.f,1])
                        X2=M2.variable('X2',Domain.inPSDCone(K.s))
                        M2.objective(ObjectiveSense.Minimize, Expr.add(Expr.dot(c1,X1),Expr.dot(c2,X2)) )        
                        M2.constraint(Expr.sub(Expr.add(Expr.mul(A1.T,X1),Expr.mul(sos.At.T,X2.reshape(K.s**2,1))), b), Domain.equalsTo(0.0))
                        M2.setLogHandler(sys.stdout)
                        M2.solve()
                        info=M2.getProblemStatus()
                        
                        if info!=ProblemStatus.PrimalAndDualFeasible:
                            x=[]
                            x2=[]
                            
                        else:
                            x=np.asarray(X1.level())
                            x2=np.asarray(X2.level())
                    

                    x1=x
                    sos.soldecvar=x

                    ptemp=sos.polynomial
                    if x==[]:
                        info='Unfeasible Problem'
                        Q=[]
                        Zmon=[]

                    else:
                        for i in range(len(x)):
                            ptemp=ptemp.subs(sos.decvartable[i],x[i])
                        Q=[]
                        Zmon=[]

                        symexpri,decvartablei,varmati,vartablei=polystr(ptemp)
                        Ati,bi,Zi,sosi=getequation(symexpri,decvartablei,varmati,vartablei)
                        sosi.polynomial=ptemp
                        sosi.flag_findsos=1
                        positivity=veryfing(sosi,'mosek')
                        if positivity>0:
                            info='Unfeasible Problem'
                   
                #3rd case
                
                elif sos.type=='eq':

                    if unfeasible==0:
                       
                        if len(sos.obj)!=0:
                            for j in range(len(sos.obj)):
                                for i in range(len(sos.decvartable2)):
                                    if sos.obj[j].coeff(sos.decvartable2[i])!=0:
                                        c[i][0]=sos.obj[j].coeff(sos.decvartable2[i])
                                        
                        c=Matrix.dense(c)
                        Kf=len(Attemp)
                        with Model("SDP3") as M3:
                            X1=M3.variable([Kf,1])   
                            M3.objective(ObjectiveSense.Minimize, Expr.dot(c,X1) ) 
                            A1=Attemp.T
                            M3.constraint(Expr.sub(Expr.mul(A1,X1), b), Domain.equalsTo(0.0)) 
                            M3.setLogHandler(sys.stdout)
                            M3.solve()
                            info=M3.getProblemStatus()
                            if info!=ProblemStatus.PrimalAndDualFeasible:
                                x1=[]
                                x2=[]
                            else:
                                x1=np.asarray(X1.level())
                                x2=[]
                            
                       
                        ptemp=sos.polynomial
                        
                        if x1==[]:
                            info='Unfeasible Problem'
                            unfeasible=1
                        else:

                            for i in range(len(x1)):
                                ptemp=ptemp.subs(sos.decvartable[i],x1[i])
                            Q=[]
                            Zmon=[]
                       
                    if unfeasible==1:
                        Q=[]
                        Zmon=[]
                        ptemp=sos.polynomial
                        x1=[]
                        x2=[]
            #4th case
            
            elif sos.nconstraint>1:

                At=sos.Atcon
                b=sos.bcon
                c=sos.ccon
                
                class K:
                    s=[]
                    f=0  
                K.f=len(sos.decvartable2) 
                K.s=sos.Ks
                
                if sos.flag_interval!=0:
                    K.s=[]
                    for i in range(sos.extravarnum2):
                        sizeX=int(np.ceil((sos.extravaridx2[i+1]-sos.extravaridx2[i])**0.5))
                        
                        K.s=np.concatenate((K.s,int(sizeX)),axis=None)
                    K.s=K.s.astype(int)    
                
                #Creating c1 and c2
                c1=c[0:K.f]
                c1=Matrix.dense(c1)
                c2=c[K.f:len(c)]
                #Creating A1 and A2
                A1=np.zeros((K.f,At.shape[1]))
                A1[:][:]=At[0:K.f][:]
                A2=np.zeros((At.shape[0]-K.f,At.shape[1]))
                A2[:][:]=At[K.f:At.shape[0]][:]
                A1=A1.T
                inindex=np.zeros((1,len(K.s)+1))
                for i in range(len(K.s)):
                    inindex[0][i+1]=inindex[0][i]+K.s[i]**2


                var_holder2 = {}
                for i in range(len(K.s)):
                    var_holder2['A2_' + str(i)]=np.zeros((int(K.s[i]**2),A2.shape[1]))
                    var_holder2['A2_' + str(i)][:][:]=A2[int(inindex[0][i]):int(inindex[0][i+1])][:]
                locals().update(var_holder2)
                
                with Model("SDP4") as M4:
                    X1=M4.variable([K.f,1])
                    objective=Expr.dot(c1, X1)
                    #Creating the variables X_i
                    var_holder = {}
                    for i in range(len(K.s)):
                        var_holder['X_' + str(i)]=M4.variable('X_%d'%i,Domain.inPSDCone(K.s[i]))
                        objective=Expr.add(objective,Expr.dot(Matrix.dense(c2[int(inindex[0][i]):int(inindex[0][i+1])]), var_holder['X_' + str(i)]))
                    locals().update(var_holder)
                    M4.objective(ObjectiveSense.Minimize, objective )
                    coni=0
                    if len(K.s)!=0:
                            for i in range(len(K.s)):
                                coni=Expr.add(coni,Expr.mul(var_holder2['A2_' + str(i)].T,var_holder['X_' + str(i)].reshape(K.s[i]**2,1)))

                            coni=Expr.add(coni,Expr.mul(A1,X1))
                            M4.constraint(Expr.sub(coni, b.T), Domain.equalsTo(0.0))
                            coni=0
                    else:
                        M4.constraint(Expr.mul(A1,X1), Domain.equalsTo(b.T))
                    
                    M4.setLogHandler(sys.stdout)
                    M4.solve()
                    info=M4.getProblemStatus()
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        x=[]
                        x1=[]
                        x2=[]
                    else:
                        x=np.asarray(X1.level())
                        x1=x
                        x2=[]

               
                sos.soldecvar=x
                Attemp=A1
                Q=[]
                Zmon=[]
                
                
                if x1==[]:
                    info='Unfeasible Problem'
                    unfeasible=1

                if unfeasible==1:
                        Q=[]
                        Zmon=[]
                        ptemp=sos.polys
                        x1=[]
                        x2=[]


                #Veryfing the result:
                for i in range(len(sos.cons)):
                    if sos.cons[i]=='ineq':
                        for j in range(len(x1)):
                            sos.polys[i]=sos.polys[i].subs(sos.decvartable2[j],x1[j])
                         
                        if sympify(sos.polys[i]).is_number:
                            if sos.polys[i]<0:
                                info='Unfeasible Problem' 
                        else:
                           
                            symexpri,decvartablei,varmati,vartablei=polystr(sos.polys[i])
                            Ati,bi,Zi,sosi=getequation(symexpri,decvartablei,varmati,vartablei)
                            
                            sosi.polynomial=sos.polys[i]
                            sosi.flag_findsos=1
                            positivity=veryfing(sosi,'mosek')
                            if positivity>0:
                                info='Unfeasible Problem'
                            

                    elif sos.cons[i]=='eq':
                        for j in range(len(x1)):
                            sos.polys[i]=sos.polys[i].subs(sos.decvartable2[j],x1[j][0])
                        if sympify(sos.polys[i]).is_number==False:
                            info='Unfeasible Problem'

                ptemp=sos.polys
                if info=='Unfeasible Problem':
                        Q=[]
                        Zmon=[]
                        ptemp=[]
                        x1=[]
                        x2=[]
                           
    else:
        if sos.nconstraint==1:
            I=1
            sos.varidx=[len(sos.decvartable) +1] 
            sos.extravaridx[0]=sos.varidx[sos.varnum+1]
            if len(sos.decvartable)>0:
                #5th case
                if sos.type=='ineq':
                    sos=addmultvar(sos,I)
                    At=sos.At
                    b=sos.b
                    c=np.zeros((At.shape[0],1))
                    
                    
                    if len(sos.obj)!=0:
                        for j in range(len(sos.obj)):
                            for i in range(len(sos.decvartable2)):
                                if sos.obj[j].coeff(sos.decvartable2[i])!=0:
                                    c[i][0]=sos.obj[j].coeff(sos.decvartable2[i])
                    class K:
                        s=[]
                        f=0   
                    K.s=(sos.extravaridx[1]-sos.extravaridx[0])**0.5
                    K.s=int(np.ceil(K.s))

                    K.f=len(sos.decvartable)
                    c1=c[0:K.f]
                    c2=c[K.f:len(c)]
                    c2=np.reshape(c2, (K.s, K.s))  
                    c1=Matrix.dense(c1)
                    c2=Matrix.dense(c2)
                    
                    
                    with Model("SDP5") as M5:
                        X1=M5.variable([K.f,1])
                        X2=M5.variable('X2',Domain.inPSDCone(K.s))
                        A1=At[0:K.f][:]
                        A2=At[K.f:At.shape[0]][:]
                        M5.objective(ObjectiveSense.Minimize, Expr.add(Expr.dot(c1,X1),Expr.dot(c2,X2)) )        
                        M5.constraint(Expr.sub(Expr.add(Expr.mul(A1.T,X1),Expr.mul(A2.T,X2.reshape(K.s**2,1))), b), Domain.equalsTo(0.0))
                        M5.setLogHandler(sys.stdout)
                        M5.solve()
                        info=M5.getProblemStatus()
                        if info!=ProblemStatus.PrimalAndDualFeasible:
                            x=[]
                            x2=[]
                        else:
                            x=np.asarray(X1.level())
                            x2=np.asarray(X2.level())
                    
                    x1=x
                    sos.soldecvar=x
                    
                    
                    ptemp=sos.polynomial
                    if x1==[]:
                        
                        info='Unfeasible Problem'
                        Q=[]
                        Zmon=[]
                        Attemp=A1
                    else:
                        for i in range(len(x)):
                            ptemp=ptemp.subs(sos.decvartable[i],x[i])
                       
                        Q=[]
                        Zmon=[]
                        Attemp=A1

                        
                        symexpri,decvartablei,varmati,vartablei=polystr(ptemp)
                        Ati,bi,Zi,sosi=getequation(symexpri,decvartablei,varmati,vartablei)
                        sosi.polynomial=ptemp
                        sosi.flag_findsos=1
                        positivity=veryfing(sosi,'mosek')
                       
                        if positivity>0:
                            
                            info='Unfeasible Problem'
                   
                #6th case
                elif sos.type=='eq':
                    At=sos.At
                    b=sos.b
                    c=np.zeros((At.shape[0],1))
                   
                    if len(sos.obj)!=0:
                        for j in range(len(sos.obj)):
                            for i in range(len(sos.decvartable2)):
                                if sos.obj[j].coeff(sos.decvartable2[i])!=0:
                                    c[i][0]=sos.obj[j].coeff(sos.decvartable2[i])
                    c=Matrix.dense(c)
                    Kf=len(sos.decvartable)
                    
                    with Model("SDP6") as M6:
                            X1=M6.variable([Kf,1])   
                            M6.objective(ObjectiveSense.Minimize, Expr.dot(c,X1) ) 
                            A1=At.T
                            M6.constraint(Expr.sub(Expr.mul(A1,X1), b), Domain.equalsTo(0.0)) 
                            M6.setLogHandler(sys.stdout)
                            M6.solve()
                            info=M6.getProblemStatus()
                            if info!=ProblemStatus.PrimalAndDualFeasible:
                                x1=[]
                                x2=[]
                            else:
                                x1=np.asarray(X1.level())
                                x2=[]
                    
                   
                    ptemp=sos.polynomial
                    
                    unfeasible=0
                    if x1==[]:
                        
                        info='Unfeasible Problem'
                        unfeasible=1
                    else:
                        
                        for i in range(len(x1)):
                            
                            ptemp=ptemp.subs(sos.decvartable[i],x1[i])
                        if sympify(ptemp).is_number==False:
                            info='Unfeasible Problem'
                            unfeasible=1
                        Q=[]
                        Zmon=[]
                        Attemp=A1
                        x=[]
                    if unfeasible==1:
                        Attemp=[]
                        Q=[]
                        Zmon=[]
                        ptemp=sos.polynomial
                        x1=[]
                        x2=[]
                        x=[]
                    
            #7th case        
            elif sos.flag_findsos==1:
                
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
                
               
                #Solving the problem
                with Model("SDP7") as M7:

                    X=M7.variable('X',Domain.inPSDCone(K.s))
                    M7.objective(ObjectiveSense.Minimize, Expr.dot(c,X))
                    M7.constraint(Expr.sub(Expr.mul(At.T,X.reshape(K.s**2,1)), b), Domain.equalsTo(0.0))
                    M7.setLogHandler(sys.stdout)
                    M7.solve()
                    info=M7.getProblemStatus()
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        x=[]
                    else:        
                        x=np.asarray(X.level())
                
               
                if x==[]:
                    info='Unfeasible Problem'
                    Attemp=[]
                    Q=[]
                    Zmon=[]
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
                        
                        
                        Zmontemp=TensorProduct(np.asarray(sos.vartable),ones(sos.extravarZ.shape[0],1))**sos.extravarZ
                        Zmon=zeros(Zmontemp.shape[0],1)
                        for i in range(Zmontemp.shape[0]):
                            Zmon[i]=prod(Zmontemp[i][:])

                    else:
                        flag_positivity+=1
                        info='Unfeasible Problem'


                    Attemp=[]
                    ptemp=sos.polynomial

                    if flag_positivity>0:
                        info='Unfeasible Problem'
                        Attemp=[]
                        ptemp=[]
                        Q=[]
                        Zmon=[]
                        info=[]
                        x=[]
                    
        #8th case        
        elif sos.nconstraint>1 : #Multiconstraints
            
                At=sos.Atcon
                b=sos.bcon
                c=sos.ccon
                
               
                class K:
                    s=[]
                    f=0  
                K.f=len(sos.decvartable2) 
                K.s=sos.Ks
                
                #Creating c1 and c2
                c1=c[0:K.f]
                c1=Matrix.dense(c1)
                c2=c[K.f:len(c)]
                #Creating A1 and A2
                A1=np.zeros((K.f,At.shape[1]))
                A1[:][:]=At[0:K.f][:]
                A2=np.zeros((At.shape[0]-K.f,At.shape[1]))
                A2[:][:]=At[K.f:At.shape[0]][:]
                A1=A1.T
                inindex=np.zeros((1,len(K.s)+1))
                for i in range(len(K.s)):
                    inindex[0][i+1]=inindex[0][i]+K.s[i]**2

                
                
                var_holder2 = {}
                for i in range(len(K.s)):
                    var_holder2['A2_' + str(i)]=np.zeros((int(K.s[i]**2),A2.shape[1]))
                    var_holder2['A2_' + str(i)][:][:]=A2[int(inindex[0][i]):int(inindex[0][i+1])][:]
                locals().update(var_holder2)
                
                with Model("SDP8") as M8:
                   
                    X1=M8.variable([K.f,1])
                    objective=Expr.dot(c1, X1)
                    #Creating the variables X_i
                    var_holder = {}
                    for i in range(len(K.s)):
                        var_holder['X_' + str(i)]=M8.variable('X_%d'%i,Domain.inPSDCone(K.s[i]))
                        objective=Expr.add(objective,Expr.dot(Matrix.dense(c2[int(inindex[0][i]):int(inindex[0][i+1])]), var_holder['X_' + str(i)]))
                    locals().update(var_holder)
                    
                    M8.objective(ObjectiveSense.Minimize, objective )
                    coni=0
                    if len(K.s)!=0:
                        for i in range(len(K.s)):
                            coni=Expr.add(coni,Expr.mul(var_holder2['A2_' + str(i)].T,var_holder['X_' + str(i)].reshape(K.s[i]**2,1)))

                        coni=Expr.add(coni,Expr.mul(A1,X1))
                        M8.constraint(Expr.sub(coni,b), Domain.equalsTo(0.0))
                        
                        coni=0
                    else:
                        M8.constraint(Expr.mul(A1,X1), Domain.equalsTo(b))
                        
                    
                    M8.setLogHandler(sys.stdout)
                    M8.solve()
                    info=M8.getProblemStatus()
                    if info!=ProblemStatus.PrimalAndDualFeasible:
                        x=[]
                        x1=[]
                        x2=[]
                    else:
                        x=np.asarray(X1.level())
                        x1=x
                        x2=[]

             
                sos.soldecvar=x
                Attemp=A1
                Q=[]
                Zmon=[]

                unfeasible=0
                if x1==[]:
                    info='Unfeasible Problem'
                    unfeasible=1

                if unfeasible==1:
                        Q=[]
                        Zmon=[]
                        ptemp=sos.polys
                        x1=[]
                        x2=[]
                if unfeasible==0:
                    
                    #Veryfing the result:
                    
                    for i in range(len(sos.cons)):
                        if sos.cons[i]=='ineq':

                            for j in range(len(x1)):
                                sos.polys[i]=sos.polys[i].subs(sos.decvartable2[j],x1[j])

                            if sympify(sos.polys[i]).is_number:
                                if sos.polys[i]<0:
                                    info='Unfeasible Problem' 

                            #TEST
                            '''
                            symexpri,decvartablei,varmati,vartablei=polystr(sos.polys[i])
                            Ati,bi,Zi,sosi=getequation(symexpri,decvartablei,varmati,vartablei)
                            sosi.polynomial=sos.polys[i]
                            sosi.flag_findsos=1
                            positivity=veryfing(sosi,'mosek')
                            '''
                            positivity=0
                            
                            if positivity>0:
                                info='Unfeasible Problem'

                        
                    
                    ptemp=sos.polys
                    if info=='Unfeasible Problem':
                            Q=[]
                            Zmon=[]
                            ptemp=[]
                            x1=[]
                            x2=[]
                                      
    class sol:
        x=[]
        decvar=[]
        Q=[]
        Zmon=[]
        info=[]
        polynomial=[]
        decvartable=[]
    if len(Attemp)!=0:
        sol.x=Z=np.concatenate((x1, x2), axis=None)
        sol.decvar=x1
    else:
        sol.x=x
        sol.decvar=[]
    sol.Q=Q
    sol.Zmon=Zmon
    sol.info=info
    sol.polynomial=ptemp
    if sos.nconstraint==1:
        sol.decvartable=sos.decvartable
    else:
        sol.decvartable=sos.decvartable2
    

    if sol.info=='Unfeasible Problem':
        print('Unfeasible Problem')
        sol.x=x
        sol.decvar=[]
        sol.Q=Q
        sol.Zmon=[]
        sol.info=[]
        sol.polynomial=[]
        

    
    return sol