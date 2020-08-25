from functools import wraps
from inspect import signature, _empty


def _adapt_get(func):
    @wraps(func)
    def wrapped(self, key):
        return func(self, *key)
    return wrapped


def _adapt_set(func):
    @wraps(func)
    def wrapped(self, key, value):
        func(self, value, *key)
    return wrapped


def _adapt_del(func):
    @wraps(func)
    def wrapped(self, key):
        func(self, *key)
    return wrapped


def _adapt_item_dunders(cls):
    for m_name, adapter, n_params in zip(("getitem", "setitem", "delitem"),
                                         (_adapt_get, _adapt_set, _adapt_del),
                                         (2, 3, 2),
                                         ):
        m_dunder = f"__{m_name}__"
        if method := getattr(cls, m_dunder, None):
            if all(p.default==_empty for p in signature(method).parameters.values()) \
                    and len(signature(method).parameters)==n_params:
                return
            setattr(cls, m_dunder, adapter(method))


class SigDepMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        _adapt_item_dunders(cls)


def signature_dependent_semantics(cls):
    _adapt_item_dunders(cls)
    return cls
