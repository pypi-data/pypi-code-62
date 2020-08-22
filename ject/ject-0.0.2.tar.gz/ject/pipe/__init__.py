import functools


def pipe(*funcs, initial_func=None):
    return functools.reduce(lambda prev, curr: (lambda x: curr(prev(x))), funcs, initial_func) \
        if initial_func else \
        functools.reduce(lambda prev, curr: (lambda x: curr(prev(x))), funcs)
