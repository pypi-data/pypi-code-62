"""Utility functions for common tasks when composing functions."""

__version__ = "0.5.0"
__all__ = (
    "compose",
    "pipe",
    "also",
    "keep",
    "drop",
    "each",
    "sort",
    "mask",
    "flat",
    "unique",
    "attrs",
    "items",
)

from operator import attrgetter as attrs
from operator import itemgetter as items


def compose(*fns):
    """Compose functions. `compose(f, g, h)(x)` is equivalent to `f(g(h(x)))`"""
    def apply(x):
        for f in reversed(fns):
            x = f(x)
        return x
    return apply


def pipe(*fns):
    """Compose functions. `pipe(f, g, h)(x)` is equivalent to `h(g(f(x)))`"""
    def apply(x):
        for f in fns:
            x = f(x)
        return x
    return apply


def also(fn):
    """Call `fn` with some input, and return the input to `fn`."""
    def inner(x):
        fn(x)
        return x
    return inner


def mask(selectors):
    """Keep items where the corresponding selector is truthy."""
    from itertools import compress
    return lambda it: compress(it, selectors)


def keep(check):
    """Yield items of the iterable where `check(item)` succeeds."""
    return lambda it: filter(check, it)


def drop(check):
    """Yield items of the iterable where `check(item)` fails."""
    from itertools import filterfalse
    return lambda it: filterfalse(check, it)


def each(fn):
    """Yield the result of applying `fn` to each item of an iterable."""
    return lambda it: map(fn, it)


def sort(_=None, /, *, key=None, reverse=False):
    """Get a sorted list of the input iterable."""
    if _ is not None:
        return sorted(_, key=key, reverse=reverse)

    return lambda it: sorted(it, key=key, reverse=reverse)


def flat(_=None, /, *, depth=1, scalar=(str, bytes, set, dict)):
    """Flatten a sequence of regular or irregular depth.

    `scalar` types are treated as single, even if iterable.
    """
    from collections.abc import Iterable

    def flattener(iterable):
        if depth <= 0:
            yield from iterable
            return

        for item in iterable:
            if isinstance(item, Iterable) and not isinstance(item, scalar):
                yield from flat(item, depth=depth-1, scalar=scalar)
            else:
                yield item

    if _ is None:
        return flattener

    return flattener(_)


def unique(_=None, /, *, key=None):
    """Yield all unique items of an iterable."""
    from collections.abc import Hashable

    def inner(iterable):
        hashables = set()
        unhashables = []

        for item in iterable:
            value = item if not key else key(item)

            if isinstance(value, Hashable):
                if value in hashables:
                    continue
                hashables.add(value)
            else:
                if value in unhashables:
                    continue
                unhashables.append(value)

            yield item

    if _ is None:
        return inner

    return inner(_)
