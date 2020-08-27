"""
    Module containing functions involed in number theory:
        ** isEven(x) x%2==0
        ** isOdd(x) x%2!=0
        ** isPrime(x)
        ** GCD(*nums) #Euclid's Algorithm for Greatest Common Divisior
        ** LCM(*nums) #Probably Another algorithm of Euclid, getting the Least Common Multiple
        ** kCn(k,n) #k chose n, the binomial coefficient
"""

from .basic import product
from typing import Union
from . import functions

def isEven(num : int) -> bool:
    """Returns True if a number can be divded by 2"""
    return num%2==0

def isOdd(num : int) -> bool:
    """Returns True if a number cannot be divded by 2"""
    return not isEven(num)

def isPrime(num : int) -> bool:
    """Returns True if a number can divide num in the \n
       ** range(2,int(1+num**(1/2))) **
       """
    if num == 1:
        return False

    for i in range(2,int(1+num**(1/2))):
        if(num%i==0):
            return False
    return True

def GCD_SIMPLE(num1 : int,num2 : int) -> int:
    """Find the greatest common multiple of 2 numbers"""
    divisor = num1 if num1 > num2 else num2
    dividor =  num1 if num1 != divisor else num2
    
    remainder = divisor%dividor
    times_in = divisor//dividor

    while remainder != 0:
        divisor = dividor
        dividor = remainder
        remainder = divisor%dividor
    
    return dividor

def GCD(*nums : int) -> int:
    """Uses Euclid's algorithm for finding the \n
       Greatest Common Multiple of a series of numbers, \n
       you can either pass arguments normally GCD(num1,num2,num3) \n
       or as a list using the * notation GCD(*myArray)
    """
    g1 = 0
    x = list(nums)
    while len(x) > 1:
        g1 = GCD_SIMPLE(x[0],x[1])
        x.pop(0)
        x.pop(0)
        x.insert(0,g1)
    return x[0]

def LCM(*args: Union[int, list]) -> int:
    """
        Given an array of integers or integers passed as arguments it can find the \n
        Least common multiple of those numbers, The smallest positive integer 'num_target' such that : \n
        (item%num_target==0 for item in args )
    """
    args = args[0] if len(args) == 1 else args

    # if the input is one number the outpout is the same number
    if (type(args) == int):
        return args

    state = {}
    nums = []

    # Create an Object keeping track of their state
    for item in args:
        state[item] = item

    def validState():
        """Checks if the object is in final format"""
        for item in state:
            if state[item] != 1:
                return False
        return True

    k = 1
    DIVISORS = []

    # Continue too loop through prime numbers while the state is not True
    while not validState():

        isAppended = False
        DIVISORS = []

        # Skip if not prime
        if not isPrime(k):
            k += 1
            continue

        for item in state:
            num = state[item]

            if num == 1:
                # Instance of object is in its final form
                DIVISORS.append(False)
                continue

            # when num is divisible by k we append k to nums[] and reduce the state
            if num % k == 0:
                state[item] = num / k  # State is reduced by k
                DIVISORS.append(True)
                if not isAppended:
                    nums.append(k)
                    isAppended = True
            else:
                DIVISORS.append(False)
        if not True in DIVISORS:
            k += 1
    return product(*nums)

def kCn(k : int,n : int) -> Union[int,float]:
    # (7,3)
    return functions.factorial(k) / (functions.factorial(n) * functions.factorial(k-n) ) 

if __name__ == "__main__": 
    print(kCn(7,3))
