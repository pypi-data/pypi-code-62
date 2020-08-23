from .backends import DefaultSignalBackend
from ._signature import PosOrKeywordSignalSignature


class Signal:
    """
    Main entity of notify lib.
    Provides descriptor that works with backend(real signal) and signature.
    """
    backend_cls = DefaultSignalBackend
    signature_cls = PosOrKeywordSignalSignature

    def __init__(self, **kwargs):
        self._name: str = ''
        self._signature = self.signature_cls(**kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.setdefault(self._name, self.backend_cls(self._name, self._signature))

    def __set_name__(self, owner, name):
        self._name = name
