#!/usr/bin/env python3

import random

# Generates a random digit ranging from 0 to 9 (Digits in Decimal Number System) and returns it as a string. 
def randdigit():
    return str(random.randint(0, 9))

# Generates a random lowercase letter from the english alphabet and returns it as a string. 
def randalpha():
    choices = list(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "x", "z"])
    return str(random.choice(choices))
        
# Generates a random special character and returns it as a string. 
def randspec():
    choices = list(["@", "%", "+", "'", "!", "#", "$", "^", "?", ":", ",", "(", ")", "{", "}", "[", "]", "~", "-", "_", "."])
    return str(random.choice(choices))
    
''' 
    Return a string with random values of designated int length (Cap of 10000). 
    The random value combos are selected by using a specific string for the seed_type argument. 
    The seed_type argument value options (not case sensitive) are as follows:
        "al" - (Alphabet Lower) Random lowercase alphabet letters.
        "au" - (Alphabet Upper) Random uppercase alphabet letters.
        "dig" - (Digit) Random digits 0-9.
        "spec" - (Special) Random special characters.
        "ad" - (Alphabet Lower|Alphabet Upper|Digit) Random lowercase & uppercase alphabet letters. Random digits 0-9.
        "ads" - (Alphabet Lower|Alphabet Upper|Digit|Special) Random lowercase & uppercase alphabet letters. Random digits 0-9. Random special characters. 
    
'''

def generate(string_length, seed_type):
    if (type(string_length) is not int):
        raise TypeError("The string_length argument must be an int!")
        
    if (string_length <= 0):
        raise ValueError("The string_length argument can't be less than or equal to zero!")

    if (string_length > 10000):
        raise ValueError("The string_length argument can't be greater than 10000!")

    if (type(seed_type) is not str):
        raise TypeError("The seed_type argument isn't a string!")

    if (seed_type.lower() != "al" and seed_type.lower() != "au" and seed_type.lower() != "dig" and seed_type.lower() != "spec" and seed_type.lower() != "ad" and seed_type.lower() != "ads"):
        raise ValueError("The seed_type argument must one of the following strings - 'al', 'au', 'dig', 'spec', 'ad', 'ads' ")
        
    randstring = str("")
    string_contents = list([""]) * string_length
    i = int(0)

    if (seed_type == "al"):
        while(i < len(string_contents)): 
            string_contents[i] = randalpha()
            i += 1
    elif (seed_type == "au"):
        while(i < len(string_contents)): 
            string_contents[i] = randalpha().upper()
            i += 1           
    elif (seed_type == "dig"):
        while(i < len(string_contents)):
            string_contents[i] = randdigit()
            i += 1
    elif (seed_type == "spec"):
        while(i < len(string_contents)):
            string_contents[i] = randspec()
            i += 1
    elif (seed_type == "ad"):
        while(i < len(string_contents)):
            choices = list([randdigit(), randalpha(), randalpha().upper()])
            string_contents[i] = str(random.choice(choices))   
            i += 1
    elif (seed_type == "ads"):
        while(i < len(string_contents)):
            choices = list([randdigit(), randalpha(), randalpha().upper(), randspec()])
            string_contents[i] = str(random.choice(choices))
            i += 1

    randstring = randstring.join(string_contents)
    return randstring

# Return true if all characters in arg string are special characters.
def isspec(arg):
    if (type(arg) is not str):
        raise TypeError("The arg argument isn't a string!")
        
    spec_digits = str("@%+'!#$^?:,(){}[]~-_.")

    for digit in arg:
        if not (digit in spec_digits):
            return False

    return True

# Return true if all characters in arg string are either upper/lower alphabet, decimal or special characters.
def isads(arg):
    if (type(arg) is not str):
        raise TypeError("The arg argument isn't a string!")
        
    ads_digits = str("@%+'!#$^?:,(){}[]~-_.0123456789abcdefghijklmnopqrstuvwyxz")

    for digit in arg.lower():
        if not (digit in ads_digits):
            return False

    return True