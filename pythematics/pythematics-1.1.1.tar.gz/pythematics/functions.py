"""
    Module containing some popular mathematical functions,\n
    that either have no specific category or were just forced here:
        ** exp(x) (Taylor Expansion or just e**x) #float -> float
        ** ln(x) #float (positive or not),complex -> float,Complex
        ** log(x) look above
        ** factorial(n) #Integer -> Integer
        ** doubleFactorial(n) #Integer -> Integer
        ** fibonacci(n) #Integer -> Integer
        ** erf(x) #float -> float
        ** erfi(x) #Complex version
        ** cis(x) # cos(x) + i*sin(x)
        ** quadratic(x) #float,int -> float,complex (linear or quadratic)
"""

from . import powers
from functools import lru_cache
from .constants import e,pi
from .num_theory import isEven,isOdd
from .constants import imaginary
from typing import Union,Tuple
from . import trigonometic as trig

@lru_cache(maxsize=1000)
def factorial(n : int) -> int:
    """
    Returns the product of all the numbers in range(1,n)\n
    ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (1,0):
        return 1
    return n * factorial(n-1)


@lru_cache(maxsize=1000)
def doubleFactorial(n : int) -> int:
    """ if n is even it returns the sum of all the even numbers\n
        if n is odd it returns the sum of all the odd numbers\n
        in the range(1,n)\n
       ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (1,0):
        return 1
    return n * doubleFactorial(n-2)

@lru_cache(maxsize=1000)
def fibonacci(n : int) -> int:
    """Returns the fibbonacci function at a specific point\n
       ** Uses the built in functool's module lru_cache decorator 
    """
    if n in (0,1):
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def exp(x : float,iterations : int = 100,taylor_exapnsion=False):
    """Calulates the exponential function,\n
        if taylor_exapnsion is set to True it will do what it says,\n
        use the taylor expansion of the exp function for calculations,\n
        else it will use the stored constant e and raise it to the power,\n
        if you set taylor_exapnsion=True you can specify how many times to iterate \n
    """
    if(not taylor_exapnsion):
        return powers.power(e,x)
    return sum([powers.power(x,n) / factorial(n) for n in range(iterations)])

def ln(x : float,iterations : int = 100) -> Union[float,complex]:
    """
        Natural log function (log with base the constant e)
        it can handle either a  floating point or an imaginary number
        it uses 'infinite' sumations which you can specify the iterations
        This is the exact formula for the natural log : https://wikimedia.org/api/rest_v1/media/math/render/svg/1d9729501b26eb85764942cb112cc9885b1a6cca
        
        Here is how it handles negative values : TLDR (log(negative) = πi + ln(abs(negative)) )
        \n\t=> e**(iπ) = -1
        \n\t=> iπ*ln(e) = ln(-1)
        \n\t=> πi = ln(-1) 
        Now with the help of this rule (log(ab) = log(a) + log(b)):
          => log(negative) = πi + ln(abs(negative)) 
          # ln(-5) = ln(-1 * 5)
          # ln(-5) = ln(-1) + ln(-5)
    """
    if type(x) == complex:
        #z = a + bi
        real = x.real
        imag = x.imag
        suma = powers.power(real,2) + powers.power(imag,2)
        reduced_log = ln(suma) / 2
        inverseTan = complex(0,1) * trig.arctan(imag / real)
        return reduced_log + inverseTan

    if x < 0:
        return (imaginary * pi) + ln(abs(x),iterations=iterations)
    if x == 0:
        raise ValueError("Logarmithic functions are not defined at {}".format(x))
    total = 0
    for k in range(iterations):
        denominator = 1 / (2*k+1)
        apr = (x - 1) / (x + 1)
        final = denominator * powers.power(apr,2*k+1)
        total += final
    return 2*total

def log(of_num : float,base : float = 10) -> float:
    """
        Returns the logarithm of a number given a base (if none is proveded it defaults to 10)
        \nFor calculations it uses the following property of logs : log(a,b) = ln(a) / ln(b)
        \nThe 'of_num' parameter can also be a complex number (check the ln for more info)
    """
    return ln(of_num) / ln(base)

def erf(x : float) -> float:
    """Calculates the error function at a specific point"""
    MULTIPLIER = 2 / powers.sqrt(pi)
    total = 0
    for n in range(100):
        denominator = factorial(n) * (2*n+1)
        nominator = powers.power(-1,n) * powers.power(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def erfi(x : float) -> float:
    """Calculates  the imaginary error function at a specific point"""
    MULTIPLIER = 2 / powers.sqrt(pi)
    total = 0
    for n in range(100):
        denominator = factorial(n) * (2*n+1)
        nominator = powers.power(x,2*n+1)
        total += nominator / denominator
    return MULTIPLIER * total

def quadratic(a,b,c) -> Union[Tuple[complex],Tuple[float]]:
    """
        Gives all complex roots of a qudratic equations,
        if the equation is linear (a==0) it will return 1 real root,
        if it is qudratic it will return a tuple of the 2 anwsers,
        which are either both going to be floats or complex
    """
    if a == 0:
        return -c / b
    descriminant = powers.power(b,2) - 4*a*c
    if descriminant < 0 :
        descriminant = imaginary * powers.sqrt(abs(descriminant))
    r_0 = (-b + descriminant) / 2*a
    r_1 = (-b - descriminant) / 2*a
    return (r_0,r_1)


def cis(x : float) -> complex:
    """Returns the following operation : \n
        cos(x) + complex(0,1) * sin(x)
    """
    return trig.sin(x) + imaginary * trig.cos(x)

def main():
    print(log(100))

if __name__ == "__main__":
    print(ln(complex(3,4)))