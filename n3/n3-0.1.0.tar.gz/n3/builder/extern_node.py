import torch.nn as nn

from .. import ast


class ExternNode(nn.Module):
    def __init__(self, input, output, **kwargs):
        super().__init__()
        self._node_input = input
        self._node_output = output

        for k, v in kwargs.items():
            setattr(self, k, v)

    def forward(self, **kwargs):
        name = self.__class__.__name__
        raise NotImplementedError(f'extern node {name} is not implemented yet')

    def __repr__(self, depth=0):
        indent = ' ' * (depth * 4) + ' ' * 2
        indent_node = ' ' * ((depth+1) * 4)

        name = f'[node extern object {self.__class__.__name__}]'
        input = f'\n{indent}[input]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_input.items())
        output = f'\n{indent}[output]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_output.items())
        return name + input + output


class NodeExecutable(nn.Module):
    def __init__(self, name, input, output, tensor_graph):
        super().__init__()
        self._name = name
        self._node_input = input
        self._node_output = output
        self._tensor_graph = tensor_graph

    def __call__(self, **kwargs):
        output = {ast.Out(0, k): x for k, x in kwargs.items()}

        for node in self._tensor_graph:
            x = {k: output[n] for k, n in node._node_input.items()}
            x = node(**x)
            if not isinstance(x, dict):
                x = {'x': x}
            x = {n: x[k] for k, n in node._node_output.items()}
            output = {**output, **x}

        return {k.name: v for k, v in x.items()}

    def __repr__(self, depth=0):
        indent = ' ' * (depth * 4) + ' ' * 2
        indent_node = ' ' * ((depth+1) * 4)

        prefix = '' if depth else '* '

        name = f'{prefix}[node object {self._name}]'
        input = f'\n{indent}[input]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_input.items())
        output = f'\n{indent}[output]\n' + \
            '\n'.join(f'{indent_node}{k}: {repr(v)}'
                      for k, v in self._node_output.items())
        tensor_graph = '\n'.join(f'{indent}({id}) {n.__repr__(depth+1)}'
                                 for id, n in enumerate(self._tensor_graph))
        return name + input + output + '\n' + tensor_graph
