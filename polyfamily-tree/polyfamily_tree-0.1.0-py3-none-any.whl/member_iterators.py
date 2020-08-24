"""
Collection of iterators for iterating members.

Feed BaseMemberIterator into MemberIteratorIterator.
MemberIteratorIterator can be chained:
ex) PreorderIterator(TypeIterator(ChildrenIterator(member), SomeSubClassOfFamilyMember))
"""

from math import inf
from collections import deque
import heapq


class _MemberIterator:
    """
    Base iterator of iterator chain
    """
    def __init__(self, member):
        self._member = member

    def __iter__(self):
        raise NotImplementedError

    def __call__(self, another_member):
        return self.__class__(another_member)


class ParentIterator(_MemberIterator):
    """
    Iter parents of given member
    """
    def __iter__(self):
        for parent in self._member._relation_lst[0]:
            yield parent


class ChildrenIterator(_MemberIterator):
    """
    Iter children of given member
    """
    def __iter__(self):
        for child in self._member._relation_lst[1]:
            yield child


class FirstDegreeIterator(_MemberIterator):
    """
    Iter member's parent and children only
    """
    def __iter__(self):
        for parent in self._member.fm_get_parents():
            yield parent
        for child in self._member.fm_get_children():
            yield child


class _MemberIteratorIterator:
    """
    Iterators that accepts other iterators
    """
    def __init__(self, iterator):
        self._iterable = iterator

    def __call__(self, member):
        return self.__class__(self._iterable(member))


class LevelIterator(_MemberIteratorIterator):
    """
    Iter by level without considering hierarchical depth
    """

    def __init__(self, iterable, end_level=inf):
        """
        :param iterable: iterable object that yield a member
        :param end_level: level to end at
        """
        super().__init__(iterable)
        self._end_level = end_level

    def __iter__(self):
        que = deque([(1, m) for m in self._iterable])
        visited = set()
        while que:
            level, member = que.popleft()
            if member not in visited and level <= self._end_level:
                visited.add(member)
                que += [(level+1, m) for m in self._iterable(member)]
                yield member


class PreorderIterator(_MemberIteratorIterator):
    """
    Traverse preorder considering hierarchical depth
    """
    def __init__(self, iterable, step=inf):
        super().__init__(iterable)
        self._step = step

    def __iter__(self):
        heap = [(1, i, m) for i, m in enumerate(self._iterable)]
        next_count = len(heap)
        depth_record = {m: 1 for m in self._iterable}

        while heap:
            level, _, member = heapq.heappop(heap)
            if depth_record.get(self, 0) >= level + 1:
                continue

            for next_member in self._iterable(member):
                if depth_record.get(next_member, 0) < level + 1:
                    depth_record[next_member] = level + 1
                    heapq.heappush(heap, (level+1, next_count, next_member))
                    next_count += 1

        for member, level in sorted(depth_record.items(), key=lambda x: x[1]):
            if level <= self._step:
                yield member


class PostorderIterator(_MemberIteratorIterator):
    """
    Traverse postorder considering hierarchical depth
    """
    def __init__(self, iterable, visited=None):
        super().__init__(iterable)
        self._visited = visited

    def __iter__(self):
        if self._visited is None:
            self._visited = set()
        for member in self._iterable:
            if member not in self._visited:
                self._visited.add(member)
                for i in PostorderIterator(self._iterable(member), self._visited):
                    yield i
                yield member


class TypeFilterIterator(_MemberIteratorIterator):
    """
    Iterator that filters type
    """
    def __init__(self, iterable, typ, is_subclass_valid=True):
        """
        :param iterable: to iter
        :param typ: typ to pass to isinstance()
        :param is_subclass_valid: flag whether subclass of a given typ is valid type
        """
        super().__init__(iterable)
        if isinstance(typ, type):
            self._typ = (typ, )
        elif isinstance(typ, (list, tuple)):
            if not all([isinstance(t, type) for t in typ]):
                raise TypeError('typ has to be type or list, tuple of types')
            self._typ = tuple(typ)
        self._is_subclass_valid = is_subclass_valid

    def __iter__(self):
        for member in self._iterable:
            if self._is_subclass_valid:
                if isinstance(member, self._typ):
                    yield member
            else:
                for t in self._typ:
                    if member.__class__ == t:
                        yield member