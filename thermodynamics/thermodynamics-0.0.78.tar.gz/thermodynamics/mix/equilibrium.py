from ..helpers import eos
from ..helpers import alfaFunctions
from ..helpers.eosHelpers import A_fun, B_fun, getCubicCoefficients, getMixFugacity,getMixFugacityCoef
from ..solvers.cubicSolver import cubic_solver
from ..helpers import temperatureCorrelations as tempCorr
from ..helpers import mixing_rules

from numpy import log, exp, sqrt,absolute, array,sum
from scipy.optimize import fsolve, newton, root
from scipy.integrate import quad

def solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals',diagram=False,properties=False,heat_capacity=None):
    # Vectorization
    tc = array(tc)
    pc= array(pc)
    acentric = array(acentric)
    liq_compositions=array(liq_compositions)
    vap_compositions = array(vap_compositions)
    kij = array(kij)
    
    # Method selection
    eos_fun = eos.selector(method)
    u,w,omega_a,omega_b,L = eos_fun()

    # Alfa function selection    
    alfa_fun = alfaFunctions.selector(alfa_function)
    alfa= alfa_fun(t,tc,acentric)
    
    Ai = A_fun(t,p,tc,pc,acentric,omega_a,alfa)
    Bi = B_fun(t,p,tc,pc,omega_b)

    # Mixing rules
    mixing_rule_used = mixing_rules.selector(mixing_rule)
    A_liq,B_liq,A_i_liq,Aij_liq,dAdT_liq = mixing_rule_used(liq_compositions,tc,acentric,kij,Ai,Bi,alfa,alfa_fun,t)
    A_vap,B_vap,A_i_vap,Aij_vap,dAdT_vap = mixing_rule_used(vap_compositions,tc,acentric,kij,Ai,Bi,alfa,alfa_fun,t)


    coefficients_liq = getCubicCoefficients(A_liq,B_liq,u,w)
    coefficients_vap = getCubicCoefficients(A_vap,B_vap,u,w)
   
    z_liq= cubic_solver(coefficients_liq,diagram,B_liq)
    z_vap = cubic_solver(coefficients_vap,diagram,B_vap)

   
    z_liq = z_liq[0] if isinstance(z_liq,tuple) else z_liq
    z_vap = z_vap[1] if isinstance(z_vap,tuple) else z_vap
    
    liq_fugacity_coef = getMixFugacityCoef(z_liq,A_liq,B_liq,A_i_liq,Bi,L)
    vap_fugacity_coef = getMixFugacityCoef(z_vap,A_vap,B_vap,A_i_vap,Bi,L)
    return (liq_fugacity_coef,vap_fugacity_coef)

def bubble_temperature(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,delta_t=0.1,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals'):
    liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
    Ki = liq_fugacity_coef/vap_fugacity_coef
    Sy = sum(Ki*liq_compositions)
    E = log(Sy)
    attempts=0
    new_t=t
    new_vap_compositions = vap_compositions

    while(absolute(E) >= 1e-9):
        if(attempts == 500):
            return 'Problem can not be solved'
        t0 = new_t + delta_t                    
        liq_fugacity_coef0,vap_fugacity_coef0 = solve_eos(t0,p,tc,pc,acentric,liq_compositions,new_vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki0 =  liq_fugacity_coef0/vap_fugacity_coef0
        Sy0 = sum(Ki0*liq_compositions)
        E0 = log(Sy0)
        new_t = (new_t*t0*(E0-E))/(t0*E0-new_t*E)
        Sy = sum(Ki*liq_compositions)
        new_vap_compositions = (Ki*liq_compositions)/Sy
        liq_fugacity_coef,vap_fugacity_coef = solve_eos(new_t,p,tc,pc,acentric,liq_compositions,new_vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki = liq_fugacity_coef/vap_fugacity_coef
        Sy = sum(Ki*liq_compositions)
        E=log(Sy)
        attempts +=1
    
    return(new_t,p,liq_compositions,new_vap_compositions)
        
def bubble_pressure(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,delta_p=0.001,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals'):
    liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
    Ki = liq_fugacity_coef/vap_fugacity_coef
    Sy = sum(Ki*liq_compositions)
    E = Sy -1
    attempts=0
    new_p=p
    new_vap_compositions = vap_compositions
  
    while(absolute(E) >= 1e-9):
        if(attempts == 100):
            return 'Probleam can not be solved'
        p0=new_p*(1+delta_p)
        liq_fugacity_coef0,vap_fugacity_coef0 = solve_eos(t,p0,tc,pc,acentric,liq_compositions,new_vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki0 =  liq_fugacity_coef0/vap_fugacity_coef0
        Sy0 = sum(Ki0*liq_compositions)
        E0=Sy0-1
        new_p = (new_p*p0*(E0-E))/(p0*E0-new_p*E)
        Sy = sum(Ki*liq_compositions)
        new_vap_compositions = (Ki*liq_compositions)/Sy
        liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,new_p,tc,pc,acentric,liq_compositions,new_vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki = liq_fugacity_coef/vap_fugacity_coef
        Sy = sum(Ki*liq_compositions)
        E = Sy -1
        attempts +=1
    
    return(t,new_p,liq_compositions,new_vap_compositions)

def dew_temperature(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,delta_t=0.1,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals'):
    liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
    Ki = liq_fugacity_coef/vap_fugacity_coef
    Sx = sum(vap_compositions/Ki)
    E = log(Sx)
    attempts=0
    new_t=t
    new_liq_compositions = liq_compositions

    while(absolute(E) >= 1e-9):
        if(attempts == 500):
            return 'Probleam can not be solved'
        t0 = new_t + delta_t
        liq_fugacity_coef0,vap_fugacity_coef0 = solve_eos(t0,p,tc,pc,acentric,new_liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki0 =  liq_fugacity_coef0/vap_fugacity_coef0
        Sx0 = sum(vap_compositions/Ki0)
        E0 = log(Sx0)
        new_t = (new_t*t0*(E0-E))/(t0*E0-new_t*E)
        Sx = sum(vap_compositions/Ki)
        new_liq_compositions = vap_compositions/(Ki*Sx)
        liq_fugacity_coef,vap_fugacity_coef = solve_eos(new_t,p,tc,pc,acentric,new_liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki = liq_fugacity_coef/vap_fugacity_coef
        Sx = sum(vap_compositions/Ki)
        E = log(Sx)
        attempts +=1
    
    return(new_t,p,new_liq_compositions,vap_compositions)

def dew_pressure(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,delta_p=0.001,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals'):
    liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
    Ki = liq_fugacity_coef/vap_fugacity_coef
    Sx = sum(vap_compositions/Ki)
    E = Sx -1
    attempts=0
    new_p=p
    new_liq_compositions = liq_compositions
  
    while(absolute(E) >= 1e-9):
        if(attempts == 100):
            return 'Probleam can not be solved'
        p0=new_p*(1+delta_p)
        liq_fugacity_coef0,vap_fugacity_coef0 = solve_eos(t,p0,tc,pc,acentric,new_liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki0 =  liq_fugacity_coef0/vap_fugacity_coef0
        Sx0 = sum(vap_compositions/Ki0)
        E0=Sx0-1
        new_p = (new_p*p0*(E0-E))/(p0*E0-new_p*E)
        Sx = sum(vap_compositions/Ki)
        new_liq_compositions = vap_compositions/(Ki*Sx)
        liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,new_p,tc,pc,acentric,new_liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki = liq_fugacity_coef/vap_fugacity_coef
        Sx = sum(vap_compositions/Ki)
        E = Sx -1 
        attempts +=1
          
    return(t,new_p,new_liq_compositions,vap_compositions)

def flash(t,p,tc,pc,acentric,feed_compositions,liq_compositions,vap_compositions,v_f,kij,delta_p=0.0001,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals'):
    tau=1
    while(absolute(tau)> 1e-5):
        liq_fugacity_coef,vap_fugacity_coef = solve_eos(t,p,tc,pc,acentric,liq_compositions,vap_compositions,kij,method,alfa_function,mixing_rule)
        Ki = liq_fugacity_coef/vap_fugacity_coef
        S = sum((feed_compositions*(Ki-1))/(1+(v_f*(Ki-1))))
        S0 = sum((-feed_compositions*(Ki-1)**2)/(1+v_f*(Ki-1))**2)
        v_f = v_f-(S/S0)
        liq_compositions0 = feed_compositions/(1+v_f*(Ki-1))
        Sx=sum(liq_compositions0)
        liq_compositions = liq_compositions0/Sx
        vap_compositions0=liq_compositions0*Ki
        Sy=sum(vap_compositions0)
        vap_compositions=vap_compositions0/Sy
        tau=sum(absolute(liq_compositions*liq_fugacity_coef-vap_compositions*vap_fugacity_coef))
    
    return (t,p,feed_compositions,liq_compositions,vap_compositions,v_f)
    
