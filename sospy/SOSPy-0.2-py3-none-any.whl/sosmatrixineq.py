#SOSMATRIXINEQ --- Creates a SOS constraint from a matrix inequality constraint
# [SOSP] = sosmatrixineq(SOSP,fM)
# SOSP is the sum of squares program.
# fM is a polynomial matrix used to generate the polynomial inequality y'fMy>0


import numpy as np
import sympy as sym
from sympy import *
from SOSTOOLSPy.sosineq import sosineq
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.getequationmc import getequationmc
from SOSTOOLSPy.sossolve2 import sossolve2

def sosmatrixineq(program,p,option):
    if program.k+1<=program.nconstraint:
        m,n=p.shape

        if m!=n:
            print('Error: Matrix fM in inequality fM>0 must be square.')
        else: 
            if option==[]:
                option='quadraticMineq' # sets the default: asks for sos expression v'M(x)v

            if option=='quadraticMineq':
                #creates the vector of variables Mvar to generate the quadratic expression M_var'*fM*Mvar

                var_holder = {}
                vartable=[]
                varMconst=zeros(n,1)
                for i in range(n):
                    var_holder['Mvar_' + str(i)]=sym.Symbol('Mvar_%d'%(i+1))
                    varMconst[i,0]=var_holder['Mvar_' + str(i)]
                    vartable=np.append(vartable,var_holder['Mvar_' + str(i)])
                locals().update(var_holder)

                expr=expand((varMconst.T*p*varMconst)[0,0])


                vartabletemp=program.vartable
                program.nvars=len(vartable)
                program.vartable=np.concatenate((program.vartable,vartable),axis=None)
                program.var=np.concatenate((program.var,vartable),axis=None)

                program,sos=sosineq(program,expr,[])
                sos.exprtype='sparsemultipartite'
                sos.exprmultipart=Matrix([[vartabletemp,varMconst]])
                sos.symvartable=vartabletemp
                sos.varmatsymvartable=varMconst

            if option=='Mineq':
                program.ktemp+=1
                At,b,Z,sos=getequationmc(p,program.decvartable,program.vartable)
                sos.polynomial=p
                sos.type='ineq'
                index=[]

                if program.nconstraint>1:#Multiconstraints
                    sos.k=program.k
                    sos.extravarnum2=program.extravarnum
                    sos.extravaridx2=program.extravaridx
                    At,b,c=sossolve2(sos)

                    if program.k==0:
                        program.Ks=[int(np.sqrt(At.shape[0]))]
                    else:
                        program.Ks=np.concatenate((program.Ks, int(np.sqrt(At.shape[0]))), axis=None)

                    if len(index)!=0:
                        for l in range(len(index)):
                            At=np.insert(At, int(index[l]), 0, axis=0)

                    if program.k==0:

                        program.cons='ineq'
                        program.polys=p
                        program.Atcon=At
                        program.bcon=b
                        program.k=program.k+1
                    else:
                        program.cons=np.concatenate((program.cons, 'ineq'), axis=None)
                        program.polys=np.concatenate((program.polys, p), axis=None)

                        #Constructing the matrix At for the multiconstraints case
                        nrows1=abs(program.Atcon.shape[0]-len(program.decvartable))
                        nrows2=abs(At.shape[0]-len(program.decvartable))
                        for m in range(int(nrows1)):
                             At=np.insert(At, len(program.decvartable)+m, 0, axis=0)

                        Arow=np.zeros((nrows2,program.Atcon.shape[1]))
                        program.Atcon=np.append(program.Atcon, Arow, axis=0)

                        program.Atcon=np.concatenate((program.Atcon, At), axis=1)
                        program.bcon=np.concatenate((program.bcon, b), axis=None)
                        program.k=program.k+1

                    sos.Atcon=program.Atcon
                    sos.bcon=program.bcon
                    sos.ccon=np.zeros((sos.Atcon.shape[0],1))
                    sos.Ks=program.Ks
                    sos.polys=program.polys
                    sos.cons=program.cons
                    program.extravarnum=sos.extravarnum2
                    program.extravaridx=sos.extravaridx2
                else:
                    program.k=program.k+1
                sos.nconstraint=program.nconstraint
                sos.decvartable2=program.decvartable
    else: 
        print('Error: More constraints than specified')
        sos=[]
        
    
    return program,sos