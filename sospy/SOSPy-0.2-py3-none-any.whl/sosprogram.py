import numpy as np



def sosprogram(var,decvar,nconstraint):
    
    class program: 
        var=[]
        decvar=[]
        nvars=0
        ndecvars=0
        Q=[]
        Zmon=[]
        nconstraint=0
        Atcon=[]
        bcon=[]
        ccon=[]
        decvartable=[]
        k=0
        j=1
        ktemp=0
        Ks=[]
        polys=[]
        cons=[]
        extravaridx=[1]
        extravarnum=0
        interval=0
        
    program.var=var
    program.decvar=decvar
    program.nvars=len(var)
    program.ndecvars=len(decvar)
    program.nconstraint=nconstraint
    program.decvartable=decvar
    program.vartable=var    
    return program
