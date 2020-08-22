from operatorUtils import isOperator, opposite_operator, stringToOperator

def make_prefix_exp(data):
    """
    Takes json dictionary which contains an equation as input and 
    returns a list with prefix representation of equation
    """
    prefix_array = []
    def prefix_exp(data):
        for k in data:

            # case when current element is not a terminal
            if(type(data[k]) is dict and data[k] is not None):
                prefix_exp(data[k])
            # case when current element is a terminal
            else:
                prefix_array.append(stringToOperator(data[k]))
        return prefix_array
    return prefix_exp(data)

def prefixToInfix(prefix_expression):
    """
    takes an array with prefix representation of equation and return 
    string with infix representation of the equation
    """
    stack = []
    for i in range(len(prefix_expression)-1, -1,-1):
        
        # case when operator is encountered pop last two operands
        if isOperator(prefix_expression[i]):
            op1 = stack.pop()
            op2 = stack.pop()

            temp = ""
            if i <= 1:
                temp = op1 + " " + prefix_expression[i] + " " + op2
            else:
                temp = "(" + op1 + " " + prefix_expression[i] + " " + op2 + ")";
            
            stack.append(temp)
        
        # case when operator is encountered, add it to the stack
        else:
            stack.append(prefix_expression[i])
    return stack.pop()


def simplify_exp(rhs, exp):
    """
    takes string representing an equation and its right hand side as input
    returns a string representing a simplified expression 
    to solve for 'x' in that equation
    """

    simplified = []
    exp = exp.split(' ')
    exp = ",".join(exp)
    
    # remove whitespaces, x and () from the input expression
    for ch in [' ', 'x', '(', ')']:
        exp = exp.replace(ch, '')
        
    exp = exp.split(',')
    
    # remove any empty strings left
    for p in exp:
        if len(p) == 0:
            exp.remove(p)
    
    if len(exp)>3:
        i = 1
        
        while i < len(exp):
    
            if (isOperator(exp[i]) and isOperator(exp[i+1])):
    
                simplified.append(opposite_operator(exp[i])+exp[i-1]+")"+opposite_operator(exp[i+1]))
                i = i+1
    
            elif isOperator(exp[i]):
    
                simplified.append(opposite_operator(exp[i]) + exp[i-1])
    
            else:
    
                simplified.append(exp[i])

            i = i + 1
        return "("+rhs+"".join(simplified)
    return rhs+exp[:-1]
