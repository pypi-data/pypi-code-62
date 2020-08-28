from enum import Enum, auto


class WithSet:
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return f'set {self.name} = {self.value}'


class With:
    def __init__(self, name, variables):
        super().__init__()
        self.name = name
        self.variables = variables

        self._depth = 1

    def __repr__(self):
        indent = ' ' * (4 * self._depth)
        name = indent + f'with {self.name}:\n'

        indent += ' ' * 4
        variables = '\n'.join(indent + str(s) for s in self.variables.values())

        return name + variables


class NodeLetType(Enum):
    BOOL = auto()
    INT = auto()
    REAL = auto()
    DATA = auto()
    NODE = auto()
    DIM = auto()

    def __repr__(self):
        if self == self.BOOL:
            return 'bool'
        if self == self.INT:
            return 'int'
        if self == self.REAL:
            return 'real'
        if self == self.DATA:
            return 'data'
        if self == self.NODE:
            return 'node'
        if self == self.DIM:
            return 'dim'


TypeConverter = {
    NodeLetType.BOOL: lambda x: bool(x),
    NodeLetType.INT: lambda x: int(x),
    NodeLetType.REAL: lambda x: float(x),
}


class NodeLet:
    def __init__(self, name, shortcut, ty, value):
        super().__init__()
        self.name = name
        self.shortcut = shortcut
        self.ty = ty
        self.value = value

    def __repr__(self):
        shortcut = f'{self.shortcut}: ' if self.shortcut else ''
        value = self.value or '*'
        if self.ty == NodeLetType.DIM:
            ty_value = repr(self.ty)
        else:
            ty_value = f'{repr(self.ty)} {value}'
        return f'let {shortcut}{self.name} = {ty_value}'


class NodeType(Enum):
    DEFAULT = auto()
    EXTERN = auto()
    DATA = auto()
    EXEC = auto()

    def __repr__(self):
        if self == self.DEFAULT:
            return ''
        if self == self.EXTERN:
            return 'extern '
        if self == self.DATA:
            return 'data '
        if self == self.EXEC:
            return 'exec '


class Node:
    def __init__(self, name, variables, withs, children, graph):
        super().__init__()
        self.name = name
        self.variables = variables
        self.withs = withs
        self.children = children
        self.graph = graph

        self.ty = NodeType.DEFAULT

        self._depth = 0

        for c in self.children.values():
            c.increse_depth()

    def increse_depth(self):
        for c in self.children.values():
            c.increse_depth()
        for g in self.graph.values():
            g.increse_depth()

        self._depth += 1

    def __repr__(self):
        indent = ' ' * (4 * self._depth)
        name = indent + f'{repr(self.ty)}node {self.name}:\n'

        indent += ' ' * 4
        variables = '\n'.join(indent + str(v)
                              for v in self.variables.values()) + '\n'
        withs = '\n'.join(str(w) for w in self.withs.values()) + '\n'
        children = '\n'.join(str(c) for c in self.children.values()) + '\n'
        graph = '\n'.join(str(c) for c in self.graph.values()) + '\n'

        return name + variables + withs + children + graph
