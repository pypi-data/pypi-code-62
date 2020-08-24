from enum import Enum


class Type(Enum):
    NONE = "None"
    ID = "ID"
    NUMBER = "Number"
    STRING = "String"
    BOOL = "Bool"


class Operator(Enum):
    EQUALS = '=='
    NOT_EQUALS = '!='
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MOD = '%'
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_THAN_EQUALS = '>='
    LESS_THAN_EQUALS = '<='
    AND = 'and'
    OR = 'or'
    NOT = 'not'


VALID_OPERATIONS_TYPES = {
            Operator.EQUALS: [Type.ID, Type.NUMBER, Type.STRING, Type.BOOL, Type.NONE],
            Operator.NOT_EQUALS: [Type.ID, Type.NUMBER, Type.STRING, Type.BOOL, Type.NONE],
            Operator.ADD: [Type.ID, Type.NUMBER, Type.STRING],
            Operator.SUBTRACT: [Type.ID, Type.NUMBER],
            Operator.MULTIPLY: [Type.ID, Type.NUMBER],
            Operator.DIVIDE: [Type.ID, Type.NUMBER],
            Operator.MOD: [Type.ID, Type.NUMBER],
            Operator.GREATER_THAN: [Type.ID, Type.NUMBER],
            Operator.LESS_THAN: [Type.ID, Type.NUMBER],
            Operator.GREATER_THAN_EQUALS: [Type.ID, Type.NUMBER],
            Operator.LESS_THAN_EQUALS: [Type.ID, Type.NUMBER],
            Operator.AND: [Type.ID, Type.BOOL],
            Operator.OR: [Type.ID, Type.BOOL],
            Operator.NOT: [Type.ID, Type.BOOL],
        }


class Term:
    def __init__(self, _type: Type, value):
        self.type = _type
        self.value = self.__try_convert_value_to_specified_type(value)

    def __try_convert_value_to_specified_type(self, value):
        if self.type == Type.NUMBER:
            return int(value)
        elif self.type == Type.BOOL:
            return self.__to_bool(str(value))
        elif self.type == Type.STRING:
            return str(value)
        elif self.type == Type.NONE:
            return None
        else:
            return value

    def has_operator(self, operator: Operator):
        return self.type in VALID_OPERATIONS_TYPES[operator]

    @staticmethod
    def __to_bool(string: str):
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            raise ValueError('ToBool is None!')


class Operation:
    def __init__(self, first_operand: Term, second_operand: Term, operator: Operator,):
        self.first_operand = first_operand
        self.operator = operator
        self.second_operand = second_operand

    def is_valid(self):
        return self.first_operand.has_operator(self.operator) and self.second_operand.has_operator(self.operator)

    def is_either_operand_of_type_id(self):
        return self.first_operand.type == Type.ID or self.second_operand.type == Type.ID

    def perform(self) -> Term:
        if self.is_valid():
            _type = Type.NUMBER
            if self.operator == Operator.ADD:
                if self.first_operand.type == Type.STRING or self.second_operand.type == Type.STRING:
                    _type = Type.STRING
                    value = SpecHelper.append_to_formatted_string(self.first_operand.value, self.second_operand.value)
                else:
                    value = self.first_operand.value + self.second_operand.value
            elif self.operator == Operator.SUBTRACT:
                value = self.first_operand.value - self.second_operand.value
            elif self.operator == Operator.MULTIPLY:
                value = self.first_operand.value * self.second_operand.value
            elif self.operator == Operator.DIVIDE:
                value = self.first_operand.value // self.second_operand.value
            elif self.operator == Operator.EQUALS:
                _type = Type.BOOL
                value = self.first_operand.value == self.second_operand.value
            elif self.operator == Operator.NOT_EQUALS:
                _type = Type.BOOL
                value = self.first_operand.value != self.second_operand.value
            elif self.operator == Operator.AND:
                _type = Type.BOOL
                value = self.first_operand.value and self.second_operand.value
            elif self.operator == Operator.OR:
                _type = Type.BOOL
                value = self.first_operand.value or self.second_operand.value
            else:
                value = None
            return Term(_type, value)
        else:
            raise Exception(
                    "{} {} {} is not a valid operation".format(self.first_operand.type.value, self.operator.value, self.second_operand.type.value))


class UnaryOperation:
    def __init__(self, operand: Term, operator: Operator):
        self.operand = operand
        self.operator = operator

    def is_valid(self):
        return self.operand.has_operator(self.operator)

    def perform(self) -> Term:
        if self.is_valid():
            if self.operator == Operator.NOT:
                _type = Type.BOOL
                value = not self.operand.value
            elif self.operator == Operator.SUBTRACT:
                _type = Type.NUMBER
                value = -int(self.operand.value)
            else:
                _type = Type.NONE
                value = None
            return Term(_type, value)
        else:
            raise Exception("{} cannot be used with type: {}".format(self.operator.value, self.operand.type.value))


class SpecHelper:
    @staticmethod
    def to_term(obj: Term) -> Term:
        return Term(obj.type, obj.value)

    @staticmethod
    def convert_to_specular_string_format(str_to_convert: str):
        # If the string we are converting doesn't have quotes then we can just return it
        if str_to_convert[0] == '"' and str_to_convert[-1] == '"':
            return r'\"{}\"'.format(str_to_convert[1:-1])
        else:
            return r'\"{}\"'.format(str_to_convert)

    @staticmethod
    def append_to_formatted_string(formatted_str: str, append):
        return SpecHelper.convert_to_specular_string_format(formatted_str[2:-2] + str(append))
