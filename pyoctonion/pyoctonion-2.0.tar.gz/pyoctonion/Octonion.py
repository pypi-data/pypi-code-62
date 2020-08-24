import numpy as np
import sympy as sym
import math
import pyquaternion as pqu

class Octon:
    def Octonion(self,x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7):   # define Octonion
        sym.init_printing()
        theta,alpha,rho,beta,u,i,j,k,l,il,jl,kl=sym.symbols('theta alpha rho beta u i j k l il jl kl')
        r_1=[x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7]
        a_1=np.array(r_1,float)
        return a_1

    def Oct_norm(self,x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7):     # define norm
        b_1=math.sqrt(x_0**2+x_1**2+x_2**2+x_3**2+x_4**2+x_5**2+x_6**2+x_7**2)
        return b_1

    def Oct_conjugate(self,x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7):
        r_2=[x_0,-x_1,-x_2,-x_3,-x_4,-x_5,-x_6,-x_7]
        a_2=np.array(r_2,float)
        return a_2

    def Oct_mult(self,x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7,y_0,y_1,y_2,y_3,y_4,y_5,y_6,y_7):  # define octonion multiplication
        sym.init_printing()
        theta,alpha,rho,beta,u,i,j,k=sym.symbols('theta alpha rho beta u i j k')
        #from pyquaternion import Quaternion
        a=pqu.Quaternion(x_0,x_1,x_2,x_3)
        b=pqu.Quaternion(x_4,x_5,x_6,x_7)
        c=pqu.Quaternion(y_0,y_1,y_2,y_3)
        d=pqu.Quaternion(y_4,y_5,y_6,y_7)
        a_1=a*c-(d.conjugate)*b
        b_1=(d*a)+(b*(c.conjugate))
        a=self.Octonion(a_1[0],a_1[1],a_1[2],a_1[3],b_1[0],b_1[1],b_1[2],b_1[3])
        x=np.array(a,float)
        return x
    #display(x[0]+x[1]*i+x[2]*j+x[3]*k+x[4]*l+x[5]*il+x[6]*jl+x[7]*kl)
    
    def Oct_inverse(self,x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7):    # define inverse
        sym.init_printing()
        theta,alpha,rho,beta,u,i,j,k=sym.symbols('theta alpha rho beta u i j k')
        #from pyquaternion import Quaternion
        b=self.Oct_conjugate(x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7)
        c=self.Oct_norm(x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7)
        d=c**2
        e=self.Octonion(b[0]/d,b[1]/d,b[2]/d,b[3]/d,b[4]/d,b[5]/d,b[6]/d,b[7]/d)
        x=np.array(e,float)
        return x

    def oct_quad(self,p_0,p_1,p_2,p_3,p_00,p_11,p_22,p_33,t_0,t_1,t_2,t_3,t_4,t_5,t_6,t_7):
        
        sym.init_printing()
        theta,alpha,rho,beta,u,i,j,k,l,il,jl,kl=sym.symbols('theta alpha rho beta u i j k l il jl kl')
        #from pyquaternion import Quaternion

        #i_1=Quaternion(0,1,0,0)
        #j_1=Quaternion(0,0,1,0)
        #k_1=Quaternion(0,0,0,1)

        b=self.Octonion(p_0,p_1,p_2,p_3,p_00,p_11,p_22,p_33)        #define Quaternion

        c=self.Octonion(t_0,t_1,t_2,t_3,t_4,t_5,t_6,t_7)


        if b[1]==0 and b[2]==0 and b[3]==0 and b[4]==0 and b[5]==0 and b[6]==0 and b[7]==0:

            if  c[1]==0 and c[2]==0 and c[3]==0 and c[4]==0 and c[5]==0 and c[6]==0 and c[7]==0:

                d=4*c[0]-b[0]**2

                if d>0:
                    d_1=abs(math.sqrt(d/4))
                    #print("Roots of the Octonionic Quadratic equation are: "+str(-b[0]/2)+" I :where I is imaginary Octonion with norm equal to "+str(d_1))
                    print("Roots of the Octonionic Quadratic equation are: "+str(-b[0]/2)+" I :where I is imaginary Octonion with norm equal to "+str(d_1))
                    #display("Roots of the Quadratic equation are:",-b[0]/2,"+I :where I is imaginary Octonion with norm equal to",d_1)

                else:
                    e=-d
                    print("Roots of the Octonionic Quadratic equation are:"+str((-b[0]+math.sqrt(e))/2)+ " or "+str((-b[0]-math.sqrt(e))/2))
                    #display("Roots of the Quadratic equation are:",(-b[0]+sqrt(e))/2, "or",(-b[0]-sqrt(e))/2 )
            else:
                r_1=((b[0]**2-4*c[0])**2)+16*(c[1]**2 + c[2]**2 + c[3]**2+c[4]**2 + c[5]**2 + c[6]**2+c[7]**2)
                r_2=b[0]**2-4*c[0]

                print("Roots are of the form:")

                #y=Quaternion(-b[0]/2+rho/2,c[1]/rho,c[2]/rho+c[3]/rho)

                #display((-b[0]/2)+(rho/2)-c[1]*(i/rho)-c[2]*(j/rho)-c[3]*(k/rho)-c[4]*(l/rho)-c[5]*(il/rho)-c[6]*(jl/rho)-c[7]*(kl/rho))
                d1 = (-b[0]/2)+(rho/2)-c[1]*(i/rho)-c[2]*(j/rho)-c[3]*(k/rho)-c[4]*(l/rho)-c[5]*(il/rho)-c[6]*(jl/rho)-c[7]*(kl/rho)
                print(d1)

                print("OR")

                print((-b[0]/2)-(rho/2)+c[1]*(i/rho)+c[2]*(j/rho)+c[3]*(k/rho)+c[4]*(l/rho)+c[5]*(il/rho)+c[6]*(jl/rho)+c[7]*(kl/rho))


                h=math.sqrt(r_1)
                m=r_2+h
                p=math.sqrt(m/2)
                print("where "+ str(rho)+ " = "+ str(p))
                #print(rho) 
                #print("=",p)


                x_0=(-b[0]/2)-(p/2)
                x_00=(-b[0]/2)+(p/2)
                x_1=c[1]/p
                x_2=c[2]/p
                x_3=c[3]/p
                x_4=c[4]/p
                x_5=c[5]/p
                x_6=c[6]/p
                x_7=c[7]/p
                q_1=self.Octonion(x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7)
                q_2=self.Octonion(x_00,-x_1,-x_2,-x_3,-x_4,-x_5,-x_6,-x_7)
                #return print("Thus, Roots of the Octonionic Quadratic equation can be written as:",q_1,"and",q_2)
                print("Roots of the Octonionic Quadratic equation can be written as:"+str(q_1[0]+q_1[1]*i+q_1[2]*j+q_1[3]*k+q_1[4]*l+q_1[4]*il+q_1[1]*jl+q_1[1]*kl)+"and"+str(q_2[0]+q_2[1]*i+q_2[2]*j+q_2[3]*k+q_2[4]*l+q_2[4]*il+q_2[1]*jl+q_2[1]*kl))

        else:
                b_1=self.Octonion(0,b[1],b[2],b[3],b[4],b[5],b[6],b[7])
                b_11=self.Octonion(b[0]/2,b[1],b[2],b[3],b[4],b[5],b[6],b[7])
                c_11=(b[0]/2)*(b_11)
                c_1=c-c_11
                B=(self.Oct_norm(b_1[0],b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7]))**2 +2*c_1[0]
                E=(self.Oct_norm(c_1[0],c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7]))**2
                
                D_1=self.Oct_mult(0,-b[1],-b[2],-b[3],-b[4],-b[5],-b[6],-b[7],c_1[0],c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])
                D=2*D_1[0]

                if D==0:
                    if B>=2*math.sqrt(E) or B<= -2*math.sqrt(E):
                        T=0
                        N_1=(B+math.sqrt(B**2 -4*E))/2
                        N_2=(B-math.sqrt(B**2 -4*E))/2

                        Q=self.Oct_inverse(0,b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7])  
                        c_111=self.Octonion(c_1[0]-N_1,c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])
                        xx_1=self.Oct_mult(Q[0],Q[1],Q[2],Q[3],Q[4],Q[5],Q[6],Q[7],c_111[0],c_111[1],c_111[2],c_111[3],c_111[4],c_111[5],c_111[6],c_111[7])
                        xx_3=self.Octonion((-b[0]/2)-xx_1[0],-xx_1[1]-xx_1[2]-xx_1[3]-xx_1[4]-xx_1[5]-xx_1[6]-xx_1[7])
                        
                        d_111=self.Octonion(c_1[0]-N_2,c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])
                        xx_2=self.Oct_mult(Q[0],Q[1],Q[2],Q[3],Q[4],Q[5],Q[6],Q[7],d_111[0],d_111[1],d_111[2],d_111[3],d_111[4],d_111[5],d_111[6],d_111[7])
                        xx_4=self.Octonion((-b[0]/2)-xx_2[0],-xx_2[1]-xx_2[2]-xx_2[3]-xx_2[4]-xx_2[5]-xx_2[6]-xx_2[7])
                        
                        #xx_2=(-b[0]/2)-Q*(c_11-N_2)
                        #return print("Roots of the Quaternionic Quadratic equation are",xx_3,"and",xx_4)
                        print("Roots of the Octonionic Quadratic equation can be written as:"+str(xx_3[0]+xx_3[1]*i+xx_3[2]*j+xx_3[3]*k+xx_3[4]*l+xx_3[5]*il+xx_3[6]*jl+xx_3[7]*kl)+"and"+str(xx_4[0]+xx_4[1]*i+xx_4[2]*j+xx_4[3]*k+xx_4[4]*l+xx_4[5]*il+xx_4[6]*jl+xx_4[7]*kl))

                    else:
                        T_1=math.sqrt(2*math.sqrt(E)-B)
                        T_2=-math.sqrt(2*math.sqrt(E)-B)
                        N=math.sqrt(E)

                        Q_1=self.Oct_inverse(b_1[0]+T_1,b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7])
                        Q_2=self.Oct_inverse(b_1[0]+T_2,b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7])
                        c_111=self.Octonion(c_1[0]-N,c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])
                        
                        xx_1=self.Oct_mult(Q_1[0],Q_1[1],Q_1[2],Q_1[3],Q_1[4],Q_1[5],Q_1[6],Q_1[7],c_111[0],c_111[1],c_111[2],c_111[3],c_111[4],c_111[5],c_111[6],c_111[7])
                        xx_3=self.Octonion((-b[0]/2)-xx_1[0],-xx_1[1],-xx_1[2],-xx_1[3],-xx_1[4],-xx_1[5],-xx_1[6],-xx_1[7])
                        
                        xx_2=self.Oct_mult(Q_2[0],Q_1[1],Q_2[2],Q_2[3],Q_2[4],Q_2[5],Q_2[6],Q_2[7],c_111[0],c_111[1],c_111[2],c_111[3],c_111[4],c_111[5],c_111[6],c_111[7])
                        xx_4=self.Octonion((-b[0]/2)-xx_2[0],-xx_2[1],-xx_2[2],-xx_2[3],-xx_2[4],-xx_2[5],-xx_2[6],-xx_2[7])
                        
                        
                        #xx_1=(-b[0]/2)-Q_1*(c_11-N)
                        #xx_2=(-b[0]/2)-Q_2*(c_11-N)
                        #return print("Roots of the Quaternionic Quadratic equation are",(xx_3),"and",(xx_4))
                        val1 = xx_3[0]+xx_3[1]*i+xx_3[2]*j+xx_3[3]*k+xx_3[4]*l+xx_3[5]*il+xx_3[6]*jl+xx_3[7]*kl
                        val2 = xx_4[0]+xx_4[1]*i+xx_4[2]*j+xx_4[3]*k+xx_4[4]*l+xx_4[5]*il+xx_4[6]*jl+xx_4[7]*kl
                        #print "Roots of the Octonionic Quadratic equation can be written as:",xx_3[0]+xx_3[1]*i+xx_3[2]*j+xx_3[3]*k+xx_3[4]*l+xx_3[5]*il+xx_3[6]*jl+xx_3[7]*kl,"and",xx_4[0]+xx_4[1]*i+xx_4[2]*j+xx_4[3]*k+xx_4[4]*l+xx_4[5]*il+xx_4[6]*jl+xx_4[7]*kl
                        print("Roots of the Octonionic Quadratic equation can be written as:"+str(val1)+" and "+str(val2))
                else: 

                    p=np.poly1d([1,2*B,B**2 -4*E,-(D**2)])
                    rootsp=p.r


                    var=[0,1,2]

                    for n in var:
                        #print(rootsp[n])
                        if rootsp[n]>0 :
                            root=rootsp[n]

                    T_1=math.sqrt(root)
                    T_2=-math.sqrt(root)
                    N_1=(T_1**3 +B*T_1+D)/(2*T_1)
                    N_2=(T_2**3 +B*T_2+D)/(2*T_2)
                    
                    
                    
                    Q_1=self.Oct_inverse(b_1[0]+T_1,b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7])
                    Q_2=self.Oct_inverse(b_1[0]+T_2,b_1[1],b_1[2],b_1[3],b_1[4],b_1[5],b_1[6],b_1[7])
                    c_111=self.Octonion(c_1[0]-N_1,c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])
                    d_111=self.Octonion(c_1[0]-N_2,c_1[1],c_1[2],c_1[3],c_1[4],c_1[5],c_1[6],c_1[7])    
                    
                    
                    xx_1=self.Oct_mult(Q_1[0],Q_1[1],Q_1[2],Q_1[3],Q_1[4],Q_1[5],Q_1[6],Q_1[7],c_111[0],c_111[1],c_111[2],c_111[3],c_111[4],c_111[5],c_111[6],c_111[7])
                    xx_3=self.Octonion((-b[0]/2)-xx_1[0],-xx_1[1],-xx_1[2],-xx_1[3],-xx_1[4],-xx_1[5],-xx_1[6],-xx_1[7])
                        
                    xx_2=self.Oct_mult(Q_2[0],Q_2[1],Q_2[2],Q_2[3],Q_2[4],Q_2[5],Q_2[6],Q_2[7],d_111[0],d_111[1],d_111[2],d_111[3],d_111[4],d_111[5],d_111[6],d_111[7])
                    xx_4=self.Octonion((-b[0]/2)-xx_2[0],-xx_2[1],-xx_2[2],-xx_2[3],-xx_2[4],-xx_2[5],-xx_2[6],-xx_2[7])
                        
                    #Q_1=(b_1+T_1).inverse
                    #Q_2=(b_1+T_2).inverse
                    #xx_1=(-b[0]/2)-Q_1*(c_11-N_1)
                    #xx_2=(-b[0]/2)-Q_2*(c_11-N_2)
                    #print(root)
                #return print("Roots of the Quaternionic Quadratic equation :",(xx_3),"and",(xx_4))
                    print("Roots of the Octonionic Quadratic equation can be written as:"+str(xx_3[0]+xx_3[1]*i+xx_3[2]*j+xx_3[3]*k+xx_3[4]*l+xx_3[5]*il+xx_3[6]*jl+xx_3[7]*kl)+" and "+str(xx_4[0]+xx_4[1]*i+xx_4[2]*j+xx_4[3]*k+xx_4[4]*l+xx_4[5]*il+xx_4[6]*jl+xx_4[7]*kl))
                    
#octonion = Octon()

#octonion.oct_quad(0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0)

#octonion.oct_quad(2/3,0,0,-1/3,-1/3,0,0,0,-1/3,0,0,2/3,2/3,0,0,0)

#octonion.oct_quad(0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0)

#octonion.oct_quad(0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8)

#octonion.oct_quad(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)