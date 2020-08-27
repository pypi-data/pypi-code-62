from .traversable import Traversable

from typing import Generic, TypeVar, Callable, Any, List
from .functor import Functor
from .applicative import Applicative
from .utils import foldl, Arrow


S = TypeVar("S")

T = TypeVar("T")

def _map(f: Arrow[S, T], ma: List[S]) -> List[T]:
    return list(map(f, ma))


list_functor = Functor(_map)


def append(l : List[T], a: T) -> List[T]:
    return l + [a]


def sequenceA(m: Applicative, ma: List[Any]) -> Any:
    return foldl(m.liftA2(append), m.pure([]), ma)


def list_traversable(m: Applicative) -> Traversable:
    return Traversable(_map, lambda ma: sequenceA(m, ma))


