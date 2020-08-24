from math import pi, sqrt
from scipy.optimize import fsolve

def orifice_calc(Q, D, hL, rho=998.9, mu=1.11e-3):
  """Calculate the required diameter of an orifice plate to acheive a given headloss, hL.
  
  Arguments:
  Q -- design flowrate, m3/s
  D -- pipe inside diameter, m
  hL -- required headloss @ design flowrate, m
  """
  
  d2 = D # pipe inside diameter
  Cd = 0.8 # sharp edge orifice plate discharge coefficient
  g = 9.87 # m/s2, gravity
  
  def _area(d):
    return pi*d**2/4
  
  # Calculate key parameters of the parent pipe
  v2 = Q / _area(d2)
  Re2 = rho * v2 * d2 / mu # reynolds number
  if Re2 < 4000: raise Exception("Error, flow not fully turbulent")
  
  # define a flowrate error function which we be solved to equal zero
  def _flowrate_error(d1):
    # calculate area and flowrate based on assumed orifice diameter
    A1 = pi*d1**2/4
    q = Cd * A1 * sqrt(2*g*hL)
    return Q - q # error
  
  # solve for d1 starting with first guess of d2
  d1 = fsolve(_flowrate_error, d2)[0] 
  
  return d1
