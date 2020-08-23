
num1 = int(input("Please input first number: "))
num2 = int(input("Please input second number: "))


def add(a, b):
    
    return a+b
    
def sub(a, b):
    
    return a-b
    
def mult(a, b):
    
    return a*b
    
def div(a, b):
    
    return float(a/b)

print("The summation is: {}\n".format(add(num1, num2)),
      "The subtraction is: {}\n".format(sub(num1, num2)),
      "The multiplication is: {}\n".format(mult(num1, num2)),
      "The division is: {}\n".format(div(num1, num2)))