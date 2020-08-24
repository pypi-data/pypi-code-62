"""
Main module including single inheritable class `FamilyMember`
"""

from .errors import *
from .member_iterators import *
from warnings import warn


class FamilyMember:
    """
    Inheritable class adding family graph functionality to class.

    Though it uses allegory of 'family', it doesn't implement 'tree data structure'.
    Relationship in default is drawn by organizing Directed Acyclic Graph(DAG).
    This means that there is a loop-less hierarchy in between members.
    Not like tree, member of this data structure can have multiple parents
    thus the package is named 'polyfamily'

    Graph organizing members is not a concrete object.
    All participants store its vicinity relationship in itself.
    By default relationship is build bidirectional - parent knows about children while
    children knows about parent. But this can be manually tweaked using
    lower level methods like `fm_append, fm_remove`.

    Methods use prefix 'fm_' to be distinguished.
    """

    # enums
    PARENT = 0
    CHILD = 1
    DO_CHECK_LOOP = True


    # member iterators
    PARENT_ITOR = ParentIterator
    CHILDREN_ITOR = ChildrenIterator
    TYPEFILTER_ITOR = TypeFilterIterator
    PREORDER_ITOR = PreorderIterator
    POSTORDER_ITOR = PostorderIterator
    LEVEL_ITOR = LevelIterator
    FIRSTDEGREE_ITOR = FirstDegreeIterator

    def __init__(self):
        """
        Initiator

        When this class is inherited this method has to be called via super().__init__()
        """
        # do not set into these values explicitly. use methods to edit relationship
        self._relation_lst = ([], [])
        self._relation_set = (set(), set())

    @classmethod
    def _typ_check(cls, obj):
        """
        Check if member is a subclass instance of this class

        :param obj: object to check type
        :return:
        """
        if not isinstance(obj, FamilyMember):
            raise NotMemberError(obj)

    @classmethod
    def _rel_type_check(cls, kind):
        """
        Check enum describing relationship
        :param kind:
        :return:
        """
        if kind not in (cls.PARENT, cls.CHILD):
            raise UnknownRelationshipError

    @classmethod
    def _check_loop(cls, parent, child, origin=None, visited=None):
        """
        Search for loop

        Check if parent is reachable traversing from child
        :param parent: member to be parent
        :param child: member to be child
        :param origin: do not assign. for recursion
        :param visited: do not assign. for recursion
        :return:
        """
        if cls.DO_CHECK_LOOP:
            # bfs
            if visited is None:
                visited = set()
                origin = parent, child
            if parent == child: # base condition
                raise TimeParadoxError(*origin)
            for c in ChildrenIterator(child):
                if c not in visited:
                    visited.add(c)
                    c._check_loop(parent, c, origin, visited)
        return True

    """
    unidirectional manipulators:
    Lower level methods.
    These manipulates relationship record of self member only.
    ex) appending a member B as self A's child doesn't mean A is appended
    as a parent of B 
    """

    def fm_append(self, member, kind):
        """
        Append an member as a given kind of relationship

        :param member: member to append
        :param kind: description of what relationship is appending member; CHILD or PARENT
        :return:
        """
        self._typ_check(member)
        self._rel_type_check(kind)
        if kind == self.PARENT:
            self._check_loop(member, self)
        else:
            self._check_loop(self, member)

        if member in self._relation_set[kind]:
            warn(AlreadyMemberError(self, member))
            return
        self._relation_lst[kind].append(member)
        self._relation_set[kind].add(member)

    def fm_remove(self, member, kind):
        """
        Remove relationship with given member

        :param member: member to break relationship with
        :param kind: description of what relationship is removing member
        :return:
        """
        self._typ_check(member)
        self._rel_type_check(kind)
        if member not in self._relation_set[kind]:
            raise NotRelatedError(self, member, kind)
        if member in self._relation_set[kind]:
            self._relation_lst[kind].remove(member)
            self._relation_set[kind].remove(member)

    def fm_clear(self, kind):
        """
        Clear record of given relationship
        :param kind:
        :return:
        """
        self._rel_type_check(kind)
        self._relation_lst[kind].clear()
        self._relation_set[kind].clear()

    """
    bidirectional manipulators:
    These manipulates relationship record of both members.
    These are all classmembers to firmly present that they
    manipulate relationship between two members.
    ex) appending a member B as self A's child will make A a parent of B
    """

    @classmethod
    def fm_append_member(cls, parent, child):
        """
        Record new bidirectional relationship as parent-child
        :param parent: member to be a parent
        :param child: member to be a child
        :return:
        """
        parent.fm_append(child, cls.CHILD)
        child.fm_append(parent, cls.PARENT)

    @classmethod
    def fm_replace_member(cls, old, new):
        """
        Replace member while relationship preserved
        :param old:
        :param new:
        :return:
        """
        for m in (old, new):
            cls._typ_check(m)
        for p in old._relation_lst[cls.PARENT]:
            new.fm_append_member(parent=p, child=new)
            p.fm_remove(old, cls.CHILD)
        for c in old._relation_lst[cls.CHILD]:
            new.fm_append_member(parent=new, child=c)
            c.fm_remove(old, cls.PARENT)

        old.fm_clear(cls.PARENT)
        old.fm_clear(cls.CHILD)

    @classmethod
    def fm_remove_relationship(cls, member1, member2):
        """
        Try remove all relationship between two members

        Make two members not know each other
        :param member1:
        :param member2:
        :return:
        """
        if member1.fm_is_parent(member2):
            member1.fm_remove(member2, cls.CHILD)
        if member1.fm_is_child(member2):
            member1.fm_remove(member2, cls.PARENT)
        if member2.fm_is_parent(member1):
            member2.fm_remove(member1, cls.CHILD)
        if member2.fm_is_child(member1):
            member2.fm_remove(member1, cls.PARENT)

    @classmethod
    def fm_clear_parent(cls, member):
        """
        Break all relationship between self and self's parents

        :param member:
        :return:
        """
        for parent in member._relation_lst[cls.PARENT]:
            parent.fm_remove(member, cls.CHILD)
        member._relation_lst[cls.PARENT].clear()
        member._relation_set[cls.PARENT].clear()

    @classmethod
    def fm_clear_children(cls, member):
        """
        Break all relationship between self and self's children
        :return:
        """
        for child in member._relation_lst[cls.CHILD]:
            child.fm_remove(member, cls.PARENT)
        member._relation_lst[cls.CHILD].clear()
        member._relation_set[cls.CHILD].clear()

    # checker
    def fm_has_parent(self):
        """
        Check if self has any parent
        :return:
        """
        return bool(self._relation_lst[self.PARENT])

    def fm_has_child(self):
        """
        Check if self has any child
        :return:
        """
        return bool(self._relation_lst[self.CHILD])

    def fm_has_relationship(self):
        """
        Check if self has any relationship
        :return:
        """
        return self.fm_has_parent() or self.fm_has_child()

    def fm_is_parent(self, child_cand):
        """
        Check if self is parent of member
        :param child_cand: child candidate to check
        :return:
        """
        if child_cand in self._relation_set[self.CHILD]:
            return True
        return False

    def fm_is_child(self, parent_cand):
        """
        Check if self is child of member
        :param parent_cand: parent candidate to check
        :return:
        """
        if parent_cand in self._relation_set[self.PARENT]:
            return True
        return False

    @classmethod
    def fm_is_related(self, member1, member2):
        """
        Check if two members are related in any awareness
        :param member1:
        :param member2:
        :return:
        """
        if member1.fm_is_parent(member2):
            return True
        elif member1.fm_is_child(member2):
            return True
        elif member2.fm_is_parent(member1):
            return True
        elif member2.fm_is_child(member1):
            return True
        return False

    # getter
    def fm_get_child(self, idx):
        """
        Return child of given idx

        :param idx: index of desired children
        :return: child
        """
        return self._relation_lst[self.CHILD][idx]

    def fm_get_parent(self, idx):
        """
        Return parent of given idx

        :param idx: index of desired parent
        :return: parent
        """
        return self._relation_lst[self.PARENT][idx]

    def fm_get_parents(self):
        """
        Return list copy of all parents
        :return:
        """
        return self._relation_lst[self.PARENT].copy()

    def fm_get_children(self):
        """
        Return list copy of all children
        :return:
        """
        return self._relation_lst[self.CHILD].copy()

    def fm_get_roots(self, visited=None):
        """
        Return roots reachable from self

        For monopoly parent family tree, single value list will be returned.
        Else does simple BFS search and returns all roots - member that has no parent
        :param visited: do not assign, in-function variable
        :return: [single_root] or [root0, ...]
        """
        if visited is None:
            visited = set()
        roots = []
        if not self._relation_set[self.PARENT]:
            return [self]
        else:
            for p in self.fm_get_parents():
                if p not in visited:
                    visited.add(p)
                    roots += p.fm_get_roots(visited=visited)
        return roots

    def fm_get_leafs(self, visited=None):
        """
        Return leafs reachable from self

        :param visited:
        :return: [leaf0, ...]
        """
        if visited is None:
            visited = set()
        leafs = []
        if not self._relation_set[self.CHILD]:
            return [self]
        else:
            for c in self._relation_lst[self.CHILD]:
                if c not in visited:
                    visited.add(c)
                    leafs += c.fm_get_leafs(visited)
        return leafs