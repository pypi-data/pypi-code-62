# GETEQUATION --- Convert a symbolic expression to At, b, and Z  used in an SOS program.

import numpy as np
from typing import NamedTuple
import sympy as sym
from sympy import LT,LM,degree,degree_list,expand,degree
from SOSTOOLSPy.collect import collect 
from dataclasses import dataclass
from sympy.matrices import Matrix, eye, zeros, ones, diag, Transpose
from scipy.sparse import csr_matrix
from SOSTOOLSPy.ismember import ismember
from SOSTOOLSPy.sortNoRepeat import sortNoRepeat
from SOSTOOLSPy.max_kron import max_kron
from SOSTOOLSPy.polystr import polystr
from SOSTOOLSPy.getequation2  import getequation2
from sympy import sympify


def getequation(symexpr,decvartable,varmat,vartable):
    
    #  Handle Polynomial Objects including the Matrix Case
    
    decvarnum=len(decvartable)
    vartable=np.concatenate((vartable,varmat))
    cvartable=np.array(vartable).astype('str').tolist()
    cvartable=np.asarray(cvartable)
    cvartable=np.sort(cvartable)
    dimp=1 # It could be changed 
    
    #Collect symexpr = g(c)*h(x) + g0 where x are the vars in vartable,
    #c are the decision variables, and h(x) is a vector of monoms.
    #in the actual polynomial vars.  Use this to find unique
    #monomials in the polynomial variables.
    
    g,h,g0=collect(symexpr)
    
    #Then the polynomial expression was divised in three terms, such that p=g*h+g0
    h0=zeros(1,1)
    h0[0]=1
    if g0[0] != 0:
        g=g.col_join(g0)
        h=h.col_join(h0)
        
    #Define the numbers of mononials and variables in p
    nmon=symexpr.nterms
    nvar=symexpr.nvars
    
    
    
    if decvarnum==0:
        
        if len(vartable)==1:
            #Create the matrix Z, which will receive the monomials of the expression
            Z=zeros(nmon,nvar)
            Z=symexpr.degmat
        else:
             #Constructing Z
           
            polynomial=symexpr.polynomial+symexpr.coeff0
            for i in range(len(decvartable)):
                polynomial=polynomial.subs(decvartable[i],1)
            symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
            if symexprg.coeff0!=0:
                nterms=symexprg.nterms+1
            else:
                nterms=symexprg.nterms
            Z=np.zeros((nterms,len(vartable)))
            for k in range(symexprg.nterms):
                mon=LT(polynomial)
                for j in range(len(vartable)):
                    deg=degree(mon,gen=vartable[j])
                    Z[k][j]=deg
                polynomial=polynomial-LT(polynomial)
                
            
        
        nmon,nvar = Z.shape
        
         # Define coefficients
        for i in range(dimp):
            for j in range(dimp):  
                exprij=symexpr
                g,h,g0=collect(exprij)
                h0=zeros(1,1)
                h0[0]=1
                len_h=len(h)
                if g0[0] != 0:
                    g=g.col_join(g0)
                    h=h.col_join(h0)
                    len_h=len(h)-1
                #Get the coefficients of the simbolic expression    
                coefmatr=g      
                monmatr = zeros(len(h),nvar)
                idx=ismember(exprij.varname,cvartable)
                monmatr=exprij.degmat
        
        
        # Constructing At and b matrices

        
        At=zeros(decvarnum,nmon*dimp**2)
        At=np.asarray(At)
        
        
        #The vector b will receive the coefficients of the the symbolic expression

        b=g.T
        
        if len(vartable)>1:
            #Constructing Z
            polynomial=symexpr.polynomial+symexpr.coeff0
            for i in range(len(decvartable)):
                polynomial=polynomial.subs(decvartable[i],1)
            symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
            if symexprg.coeff0!=0:
                nterms=symexprg.nterms+1
            else:
                nterms=symexprg.nterms
            Z=np.zeros((nterms,len(vartable)))
            for k in range(symexprg.nterms):
                mon=LT(polynomial)
                for j in range(len(vartable)):
                    deg=degree(mon,gen=vartable[j])
                    Z[k][j]=deg
                polynomial=polynomial-LT(polynomial)
                
            
            #Constructing b
            b=np.zeros((nterms,1))
            polynomial= symexpr.polynomial+symexpr.coeff0
            
            for l in range(len(decvartable)):
                polynomial=polynomial-expand(decvartable[l]*polynomial.coeff(decvartable[l]))
           
            
            flag_coeff0=sympify(polynomial).is_number
            
            if polynomial!=0 and flag_coeff0!=True:
                symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                #Creating the vectors of degrees and coefficients
                if len(vartableg)==len(vartable):
                    if np.array_equal(vartableg, vartable)==False:
                        vartableg=vartableg[::-1]
                   
                vartableg=vartable
                      
                bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                
                
                Zgtemp1=np.zeros((Zg.shape[0],Z.shape[1]))
                
                l=0
                
                while Z.shape[1]!=Zg.shape[1]:
                    for k in range(len(vartable)):
                        if degree(polynomial,gen=vartable[k])!=0:
                            for j in range(Zg.shape[0]):
                                
                                Zgtemp1[j][k]=Zg[l]
                                l=l+1
                    Zg=Zgtemp1
                
               
                bidex=[]
                k=0
                value=[]
                
                for i in range(Zg.shape[0]):
                    if np.array_equal(Z[k][:], Zg[i][:]):
                        
                        bidex=np.concatenate((bidex, k), axis=None)
                        k=k+1
                    else:
                        value=Zg[i][:]
                        
                        while np.array_equal(Z[k][:], value)==False:
                            k=k+1
                        bidex=np.concatenate((bidex, k), axis=None)
                        k=k+1   
              
                
                for i in range(len(bidex)):
                    b[int(bidex[i])][0]=bg[i]
                        
               
            elif polynomial!=0 and flag_coeff0==True:
                b[nterms-1][0]=polynomial
                
            #Constructing At
            At=np.zeros((decvarnum,nmon*dimp**2))

       
    else:
        
       
        if len(vartable)==1:
            
            #Constructing Z
            Z=[]
            polynomial=symexpr.polynomial+symexpr.coeff0
            
            for k in range(len(decvartable)):
                if degree(polynomial.coeff(decvartable[k]))==0: 
                    Zg=[0]
                    Z=np.concatenate((Z, Zg), axis=None)
                    polynomial=polynomial-expand(decvartable[k]*polynomial.coeff(decvartable[k])) 
                else:
                    symexprg,decvartableg,varmatg,vartableg=polystr(polynomial.coeff(decvartable[k]))
                    bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                    Z=np.concatenate((Z, Zg), axis=None)
                    polynomial=polynomial-expand(decvartable[k]*polynomial.coeff(decvartable[k]))
                    if polynomial==0:
                        break

            if polynomial!=0 and degree(polynomial)!=0:   
                symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg) 
                Z=np.concatenate((Z, Zg), axis=None)
            elif polynomial!=0 and degree(polynomial)==0:
                Zg=[0]
                Z=np.concatenate((Z, Zg), axis=None)
            Z=np.unique(Z)
            Z=Z[::-1]



            #Constructing b
            polynomial=symexpr.polynomial+symexpr.coeff0

            for l in range(len(decvartable)):
                polynomial=polynomial-expand(decvartable[l]*polynomial.coeff(decvartable[l]))


            if polynomial!=0 and degree(polynomial)!=0:
                symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)

                b=np.zeros((1,Z.shape[0]))

                for m in range(len(bg)):
                    idx=Z.shape[0]-np.where(Z == Zg[m][0])[0][0]-1


                    if idx>len(b[0])-1:

                        idx=idx-1

                    b[0][idx]=bg[m]

                b=b[0][::-1]    

            elif polynomial==0 or degree(polynomial)==0 :
                ptemp=polynomial
                deg=[]
                polynomial=symexpr.polynomial + symexpr.coeff0
                #Constructing At
                for n in range(len(decvartable)):
                    deg=np.concatenate((deg, degree(polynomial.coeff(decvartable[n]))), axis=None)
                    symexpr.maxdeg=np.amax(deg)


                b=np.zeros((1,Z.shape[0]))
                b[0][0]=ptemp
                b=b[0][::-1]


            #Constructing At
            deg=[]
            polynomial=symexpr.polynomial + symexpr.coeff0
            #Constructing At
            for n in range(len(decvartable)):
                deg=np.concatenate((deg, degree(polynomial.coeff(decvartable[n]))), axis=None)
                symexpr.maxdeg=np.amax(deg)


           
            At=np.zeros((len(decvartable),int(Z[0]+1)))
            for i in range(len(decvartable)):

                if degree(polynomial.coeff(decvartable[i]))==0:
                    bg=[polynomial.coeff(decvartable[i])]
                    Zg=np.zeros((1,1))
                else:    
                    symexprg,decvartableg,varmatg,vartableg=polystr(polynomial.coeff(decvartable[i]))
                    bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                for j in range(len(bg)):
                    At[i][int(Zg[j][0])]=-bg[j]
    
        else: #Case multivars
            
            #Constructing Z
            
            
            
            polynomial=symexpr.polynomial+symexpr.coeff0
           
            symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
            if symexprg.coeff0!=0:
                nterms=symexprg.nterms+1
            else:
                nterms=symexprg.nterms
            Z=np.zeros((nterms,len(vartable)))
            for k in range(symexprg.nterms):
                mon=LT(polynomial)
                for j in range(len(vartable)):
                    deg=degree(mon,gen=vartable[j])
                    Z[k][j]=deg
                polynomial=polynomial-LT(polynomial)
           
              
            Z=np.unique(Z, axis=0)
            Z=Z[::-1]
           
            
            b=np.zeros((Z.shape[0],1))
     
            polynomial= symexpr.polynomial+symexpr.coeff0
            for l in range(len(decvartable)):
                polynomial=polynomial-expand(decvartable[l]*polynomial.coeff(decvartable[l]))
            
            
            flag_coeff0=sympify(polynomial).is_number
            
            if polynomial!=0 and flag_coeff0!=True:
                symexprg,decvartableg,varmatg,vartableg=polystr(polynomial)
                #Creating the vectors of degrees and coefficients
                if len(vartableg)==len(vartable):
                    if np.array_equal(vartableg, vartable)==False:
                        vartableg=vartableg[::-1]
                   
                vartableg=vartable
                      
                bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)
                
                
                Zgtemp1=np.zeros((Zg.shape[0],Z.shape[1]))
                
                l=0
                k=0
                while Z.shape[1]!=Zg.shape[1]:
                    for k in range(len(vartable)):
                        if degree(polynomial,gen=vartable[k])!=0:
                            for j in range(Zg.shape[0]):
                                
                                Zgtemp1[j][k]=Zg[l]
                                l=l+1
                    Zg=Zgtemp1
                
               
                bidex=[]
                k=0
                value=[]
                
                for i in range(Zg.shape[0]):
                    if np.array_equal(Z[k][:], Zg[i][:]):
                        
                        bidex=np.concatenate((bidex, k), axis=None)
                        k=k+1
                    else:
                        value=Zg[i][:]
                        
                        while np.array_equal(Z[k][:], value)==False:
                            k=k+1
                        bidex=np.concatenate((bidex, k), axis=None)
                        k=k+1   
              
                
                for i in range(len(bidex)):
                    b[int(bidex[i])][0]=bg[i]
                        
               
            elif polynomial!=0 and flag_coeff0==True:
                b[nterms-1][0]=polynomial
                
            
           
            #Constructing At
            
            polynomial=symexpr.polynomial+symexpr.coeff0
            
            At=np.zeros((len(decvartable),Z.shape[0]))
            
            for i in range(len(decvartable)):
                poly=polynomial.coeff(decvartable[i])
                
                symexprg,decvartableg,varmatg,vartableg=polystr(poly)
                
                #Creating the vectors of degrees and coefficients
                if len(vartableg)==len(vartable):
                    if np.array_equal(vartableg, vartable)==False:
                        vartableg=vartableg[::-1]
                      
                vartableg=vartable
                
                
                flag_coeff0=sympify(poly).is_number
                
                if poly!=0 and flag_coeff0!=True:
                    bg,Zg=getequation2(symexprg,decvartableg,varmatg,vartableg)

                    Zgtemp1=np.zeros((Zg.shape[0],Z.shape[1]))

                    l=0
                    k=0
                    while Z.shape[1]!=Zg.shape[1]:
                        for k in range(len(vartable)):
                            if degree(poly,gen=vartable[k])!=0:
                                for j in range(Zg.shape[0]):

                                    Zgtemp1[j][k]=Zg[l]
                                    l=l+1
                        Zg=Zgtemp1

                    Aidex=[]
                    k=0
                    value=[]
                    for c in range(Zg.shape[0]):
                        if np.array_equal(Z[k][:], Zg[c][:]):

                            Aidex=np.concatenate((Aidex, k), axis=None)
                            k=k+1
                        else:
                            value=Zg[c][:]
                            while np.array_equal(Z[k][:], value)==False:
                                k=k+1
                            Aidex=np.concatenate((Aidex, k), axis=None)
                            k=k+1   


                    for m in range(len(Aidex)):
                        At[i][int(Aidex[m])]=-bg[m]

                elif poly!=0 and flag_coeff0==True:
                    At[i][At.shape[1]-1]=-poly
                        
                        
                        
                        
            
    class sos:
        At=0
        b=0
        Z=0
        extravarZ=[]
        extravarZZ=[]
        extravarT=[]
        extravaridx=[]
        extravarnum=[]
        Zget=[]
        vartable=[]
        coeff0=[]
        decvartable=[]
        polynomial=[]
        soldecvar=[]
        type=[]
        Atcon=[]
        bcon=[]
        ccon=[]
        nconstraint=1
        decvartable2=[]
        Ks=[]
        polys=[]
        cons=[]
        varidx=[]
        varnum=[]
        exprnum=[]
        flag_findsos=[]
        obj=[]
        interval=[]
        k=0
        extravaridx2=[]
        extravarnum2=0
        flag_interval=0
        exprtype=[]
        exprmultipart=[]
        symvartable=[]
        varmatsymvartable=[]
        matrixtype=0
        
        
    sos.At=At
    sos.b=b
    sos.Z=Z
    sos.extravaridx=[1]
    sos.Zget=Z
    sos.vartable=vartable
    sos.coeff0=symexpr.coeff0
    sos.decvartable=decvartable
    sos.varnum=-1
    sos.extravarnum=0
    sos.exprnum=1
    
   
    return At,b,Z,sos
  

    
    
