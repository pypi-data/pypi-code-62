"""
Errors for `FamilyMember`
"""


class UnknownRelationshipError(KeyError):
    def __str__(self):
        return f"use self.CHILD or self.PARENT enum to describe relationship"


class AlreadyMemberError(ValueError):
    """
    Error to be warned when trying to override existing relationship
    """

    def __init__(self, a, b):
        memberA_ind = str(a) if hasattr(a, '__str__') else f"<{a.__class__.__name__} {id(a)}>"
        memberB_ind = str(b) if hasattr(b, '__str__') else f"<{b.__class__.__name__} {id(b)}>"
        self._comment = f"{memberA_ind} and {memberB_ind} are already related"

    def __str__(self):
        return self._comment


class NotRelatedError(ValueError):
    """
    Not related
    """

    def __init__(self, obj, sbj, kind):
        self._comment = f"{sbj} is not {'CHILD' if kind else 'PARENT'} of {obj}"

    def __str__(self):
        return self._comment


class NotMemberError(TypeError):
    """
    Not a subclass of FamilyMember
    """

    def __init__(self, inst):
        self._comment = f"<{inst.__class__.__name__}> is not a subclass of <FamilyMember>"

    def __str__(self):
        return self._comment


class TimeParadoxError(AttributeError):

    def __init__(self, parent, child):
        """
        Acyclicity violation between members
        :param parent: member as parent
        :param child: member as child
        """

        parent_ind = str(parent) if hasattr(parent, '__str__') else f"<{parent.__class__.__name__} {id(parent)}>"
        child_ind = str(child) if hasattr(child, '__str__') else f"<{child.__class__.__name__} {id(parent)}>"
        self._comment = f"{parent_ind} can't be a parent of {child_ind}"

    def __str__(self):
        return self._comment
