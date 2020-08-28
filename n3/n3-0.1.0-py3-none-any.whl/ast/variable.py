from enum import Enum, auto

from .graph import Out
from .node import NodeLetType


def is_estimable(value):
    if isinstance(value, (Variable, Expr)):
        return value.is_estimable()
    return value is not None


def is_hint(value):
    if isinstance(value, (Variable, Expr)):
        return value.is_hint()
    return isinstance(value, Out)


class Variable:
    def __init__(self, name, value=None):
        super().__init__()
        self.name = name
        self.shortcut = None
        self.ty = None
        self.value = value

    def assert_estimable(self):
        assert is_estimable(self.value), f'unestimable variable: {self.name}'
        return True

    def is_estimable(self):
        return is_estimable(self.value)

    def is_hint(self):
        return self.ty == NodeLetType.DIM or is_hint(self.value)

    def __repr__(self):
        if self.value is not None:
            return f'{self.name}={repr(self.value)}'
        return self.name


class Operator(Enum):
    NEG = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    AND = auto()
    OR = auto()
    XOR = auto()

    def __repr__(self):
        if self == self.NEG:
            return '-'
        if self == self.ADD:
            return '+'
        if self == self.SUB:
            return '-'
        if self == self.MUL:
            return '*'
        if self == self.DIV:
            return '/'
        if self == self.MOD:
            return '%'
        if self == self.POW:
            return '**'
        if self == self.AND:
            return '&'
        if self == self.OR:
            return '|'
        if self == self.XOR:
            return '^'


OperatorFn = {
    Operator.NEG: lambda a, _: -a,
    Operator.ADD: lambda a, b: a + b,
    Operator.SUB: lambda a, b: a - b,
    Operator.MUL: lambda a, b: a * b,
    Operator.DIV: lambda a, b: a / b,
    Operator.MOD: lambda a, b: a % b,
    Operator.POW: lambda a, b: a ** b,
    Operator.AND: lambda a, b: a & b,
    Operator.OR: lambda a, b: a ^ b,
    Operator.XOR: lambda a, b: a ^ b,
}


class Expr:
    def __init__(self, op, lhs, rhs=None):
        super().__init__()
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def is_estimable(self):
        is_estimable(self.lhs)
        if self.rhs:
            is_estimable(self.rhs)
        return True

    def is_hint(self):
        return is_hint(self.lhs) or is_hint(self.rhs)

    def __repr__(self):
        if not self.rhs:
            return f'{repr(self.op)}{self.lhs}'
        return f'({self.lhs} {repr(self.op)} {self.rhs})'


class Shape:
    def __init__(self, dims, name='x'):
        super().__init__()
        self.name = name
        self.dims = dims

    def product(self):
        value = 1
        for dim in self.dims or []:
            value = Expr(Operator.MUL, value, dim)
        return value

    def __len__(self):
        return len(self.dims)

    def __repr__(self):
        dims = ', '.join(str(d) if d else '*' for d in self.dims)
        return f' = {dims}'
