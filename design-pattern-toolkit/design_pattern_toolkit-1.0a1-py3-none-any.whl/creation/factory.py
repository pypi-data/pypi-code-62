from abc import ABC, abstractmethod
from typing import Sequence
import re
import keyword
from typing import Mapping, Any


class AbstractFactory(ABC):

    @classmethod
    @abstractmethod
    def produce(cls, product, specification):
        pass


class Factory(AbstractFactory):
    cache = dict()

    @classmethod
    def register(cls, product: Any, definition: Mapping = None) -> None:
        # @todo: Expand to accommodate production of existing classes
        if isinstance(product, type):
            if product.__qualname__ not in cls.cache:
                cls.cache.update({product.__qualname__: product})

        elif isinstance(product, str):
            word = re.compile(r'[aA-zZ0-9_]')
            # if the parameter is a string create as type else save as class
            if not word.match(product):
                raise RuntimeError(
                        'Invalid name provided. Name should be alphanumeric '
                        'and less than 50 characters')
            if product in keyword.kwlist:
                raise RuntimeError('Invalid class name. Class should not be a Python reserved '
                                   'keyword')
            if product not in cls.cache:
                definition = dict(definition)  # coarse keyword types to dictionary
                cls.cache.update({product: type(product, (object,), definition)})

    @classmethod
    def produce(cls, product: Any, specification: Mapping = None, bases: Sequence = None,
                *args, **kwargs) ->\
            Any:
        # @todo: Expand to accommodate production of existing classes
        def _create(object_, bases_, dict_):
            try:
                prototype = None
                if not isinstance(object_, str):
                    raise RuntimeError(
                        'Invalid name provided. Name should be alphanumeric')
                if not bases_:
                    if isinstance(dict_, Mapping) and dict_:
                        prototype = type(object_, (object,), dict(dict_))
                    else:
                        prototype = type(object_, (object,), {})
                elif bases_ and isinstance(bases_, Sequence):
                    parents = tuple((x for x in bases_ if isinstance(x, (str, type))))
                    if isinstance(dict_, Mapping) and dict_:
                        prototype = type(product, parents, dict(dict_))
                    else:
                        prototype = type(product, parents, {})
                return prototype
            except TypeError:
                raise
            except Exception:
                raise

        if product in cls.cache:
            instance = cls.cache.get(product)
            if instance:
                return instance(*args, **kwargs)
        else:
            instance = _create(product, bases, specification)
            return instance(*args, **kwargs)
