from inspect import signature


def length(fn):
    sig = signature(fn)
    params = sig.parameters
    return len(params)
