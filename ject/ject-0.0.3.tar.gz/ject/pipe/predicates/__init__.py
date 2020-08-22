from functools import reduce

from ject import oneself


def intersect(*predicates):
    fns = [p for p in predicates if p is not None]
    if (hi := len(fns)) == 0: return oneself
    elif hi == 1: return fns[0]
    elif hi == 2 and (a := fns[0]) and (b := fns[1]): return lambda x: a(x) and b(x)
    elif hi == 3 and (a := fns[0]) and (b := fns[1]) and (c := fns[2]): return lambda x: a(x) and b(x) and c(x)
    else: return lambda x: reduce(lambda pr, fn: pr and fn(x), fns)


def union(*predicates):
    fns = [p for p in predicates if p is not None]
    if (hi := len(fns)) == 0: return oneself
    elif hi == 1: return fns[0]
    elif hi == 2 and (a := fns[0]) and (b := fns[1]): return lambda x: a(x) or b(x)
    elif hi == 3 and (a := fns[0]) and (b := fns[1]) and (c := fns[2]): return lambda x: a(x) or b(x) or c(x)
    else: return lambda x: reduce(lambda pr, fn: pr or fn(x), fns)
