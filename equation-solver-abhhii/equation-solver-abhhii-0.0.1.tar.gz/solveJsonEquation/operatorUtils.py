def isOperator(x):
    if x in ['+', '-', '*', '/', '=']:
        return True
    return False


def stringToOperator(op_string):
    if op_string == "equal":
        return "="
    if op_string == "add":
        return "+"
    if op_string == "subtract":
        return "-"
    if op_string == "multiply":
        return "*"
    if op_string == "divide":
        return "/"
    return str(op_string)

def opposite_operator(op):
    if op == "+":
        return "-"
    if op == "-":
        return "+"
    if op == "*":
        return "/"
    if op == "/":
        return "*"
    return op    