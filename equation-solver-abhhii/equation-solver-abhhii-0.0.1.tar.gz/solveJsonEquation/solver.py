import json
from operatorUtils import isOperator, stringToOperator, opposite_operator
from expression import simplify_exp, make_prefix_exp, prefixToInfix

data = {}
# open json file containg equation data
with open("equation.json") as f:
    data = json.load(f)

# make prefix expression
prefix_arr = make_prefix_exp(data)

# convert it to infix representation and print expression
expression = prefixToInfix(prefix_arr)
print(expression)

# simplify expression
lhs = expression.split("=")[0]
rhs = expression.split("=")[1].strip()
val = simplify_exp(rhs, lhs)
print(f"x = {val}")

# evaluate expression
print(f"x = {eval(val)}")
