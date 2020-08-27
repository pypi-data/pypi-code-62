"""
    Computes powers and roots of specified numbers using Newton's approximation,
    it also handle operation with imaginary numbers

    Detail:
        ** Power : 
            ** Base : float or complex
            ** Exponent : float or complex
            returns base to the power of exponent
        ** sqrt :
            x : float or int
            return the square root of x
        ** nthRoot :
            A generilization of the sqrt function

"""

from .basic import product
from .basic import isInteger
from . import functions
from typing import Union
from . import trigonometic as trg

def floatPow(base,exponent):
    """For handling float powers"""
    total = 1
    constLog = functions.ln(base)
    for i in reversed(range(1,100)):
        total = 1 + total * exponent * constLog / i
    return total

def power(base : Union[float,complex],exponent : Union[float,complex]) -> Union[float,complex]:
    """
    The power function equivalant of the python operation a**b\n
    it can handle any floating or integer value for a base\n
    for an exponent it can handle any integer or float or complex number ,\n

    Here is how it treats complex numbers (exponents) => :
        ** e^(ix) = cos(x) + i *sin(x) #cis(x) for short
        ** e^(i*ln(a)) = cis(ln(a))
        ** e^(ln(a^i)) = cis(ln(a))
        ** a^i = cis(ln(a))
        ** (a^i)^b = (cis(ln(a)))^b
        ** a^(bi) + a^c = (cis(ln(a)))^b + a^c
        ** a^(bi+c) = (cis(ln(a)))^b + a^c
    Complex Base number is treated normally like an integer

    """
    if type(exponent) == type(complex(0,1)):
        s = exponent # a*i+b
        return power(base,s.real) + power(functions.cis(functions.ln(base)),s.imag)

    if exponent < 0:
        return 1 / power(base,-exponent)
    if not isInteger(exponent):
        if type(exponent) == float:
            return floatPow(base,exponent)
        else:
            raise ValueError("Power operations does not support {}".format(type(exponent)))
    
    x = [base for i in range(int(exponent))]
    return product(*x)

def sqrt_subfunction(x,c):
    """Function used to estimate the sqrt"""
    return power(x,2) - c

def sqrt(x : float,iterations : int = 100,catchNegativeRoot=False) -> Union[float,complex]:
    """
        Uses Newtown's method for calculating the square root of a specific number,\n
        you can specify with 'iterations' how many times you want to repeat the algorithm,\n
        if the input argument is less than 0 it will return a complex number
    """
    if x <= 0:
        if(x==0):
            return 0.0
        if catchNegativeRoot:
            raise ValueError("Value '{}' is not in the real number range".format(x))
        return complex(0,1) * sqrt(abs(x))
    point = 1
    for i in range(iterations):
        function_difference = sqrt_subfunction(point,x) / (2*point)
        point = point - function_difference
    return point

def nth_subfunction(x,exponent,c):
    """function used for the calculation of the nth root acts as a derivative"""
    return power(x,exponent) - c

def nthRoot(subroot : float,n : int,iterations : int = 100,catchNegativeRoot=False) -> float:
    """
        Uses Newtown's method for calculating the nth root function of a specific number,\n
        you can specify with 'iterations' how many times you want to repeat the algorithm,\n
        You can specify whether you want to throw an error when the result is complex,\n
        If not specified it will return the complex solution
    """
    if(n%2==0) or n==0:
        if n==0:
            return 0.0
        if subroot < 0:
            if not catchNegativeRoot:
                return trg.complexRoot(n) * nthRoot(abs(subroot),n,iterations=iterations)
            raise ValueError("Even root must contain only positive floating values not {}".format(subroot))
    
    def diffeq(x):
        raised = power(x,n-1)
        return n*raised

    point = 1
    for i in range(iterations):
        function_difference = nth_subfunction(point,n,subroot) / diffeq(point)
        point = point - function_difference

    return point

if  __name__ == "__main__":
    pass