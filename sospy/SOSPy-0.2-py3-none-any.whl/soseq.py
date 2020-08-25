import numpy as np
import sympy as sym
from sympy import degree_list,degree,LT,LM,LC,matrix2numpy,sympify,poly
from sympy import ImmutableMatrix as  Matrix
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.getequation import getequation
from SOSTOOLSPy.sossolve2 import sossolve2

def soseq(program,p):
    program.ktemp+=1
    if program.k+1<=program.nconstraint:
        
        #Analyse if all the decision vars are using in this problem
        decvartemp=[]
        symb=list(p.free_symbols)
        index2=np.isin(program.decvartable,symb)
        index=[]
        for i in range(len(index2)):
            if index2[i]==True:
                decvartemp=np.concatenate((decvartemp,program.decvartable[i]), axis=None) 
            else:
                index=np.concatenate((index,i), axis=None) 
        program.decvar=decvartemp
        
        #Analyse if all the variables are using in this problem
        vartemp=[]
        index2=np.isin(program.vartable,symb)
        for i in range(len(index2)):
            if index2[i]==True:
                vartemp=np.concatenate((vartemp,program.vartable[i]), axis=None) 
            
        program.var=vartemp
        program.nvars=len(program.var)
       
        symexpr, decvartable, varmat, vartable=polystr(p)

        if len(program.decvar)!=0: #In this case, the program has decision vars
            decvartable=program.decvar
            vartable=program.var
        if program.nvars==1: #One variable
            At,b,Z,sos=getequation(symexpr,decvartable,varmat,vartable)
            sos.Z=np.transpose([sos.Z])
            sos.b=Matrix(sos.b)
            sos.b=(sos.b).T
            sos.polynomial=p
            sos.type='eq'
        else:#Multivariable
            At,b,Z,sos=getequation(symexpr,decvartable,varmat,vartable)
            sos.polynomial=p
            sos.type='eq'



        if program.nconstraint>1:
            At,b,c=sossolve2(sos)

            
            if len(index)!=0:
                for l in range(len(index)):
                    At=np.insert(At, int(index[l]), 0, axis=0)
                    
            if program.k==0:
                program.cons='eq'
                program.polys=p
                program.Atcon=At
                program.bcon=b
                program.k=program.k+1
            else:
                program.cons=np.concatenate((program.cons, 'eq'), axis=None)
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
            sos.polys=program.polys
            sos.cons=program.cons
            sos.Ks=program.Ks
        elif len(program.decvar)==0:
            sos.flag_findsos=1
        sos.nconstraint=program.nconstraint
        sos.decvartable2=program.decvartable
        
    if program.ktemp>program.nconstraint:
        print('Error: More constraints than specified')
        sos=[]
        
    return program,sos