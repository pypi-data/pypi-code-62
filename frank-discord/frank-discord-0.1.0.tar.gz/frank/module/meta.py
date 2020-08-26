# =====IMPORTS=====
# Future imports
from __future__ import annotations

# Built-in imports
from functools import cached_property

# Own imports
from .decorators import Command, Daemon, Default, RegexCommand

# Typing imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Built-in imports
    from typing import List, Any


class ModuleMeta:
    def _filter_attrs(self, condition: callable[[Any], bool]) -> List[Any]:
        # This prevents an infinite loop of getting the attribute
        illegal_names = ['commands', 'daemons', 'default']

        output = []

        for attr in filter(lambda x: x not in illegal_names, dir(self)):
            value = getattr(self, attr)

            if condition(value):
                output.append(value)

        return output

    @cached_property
    def commands(self) -> List[Command]:
        # This also matches RegexCommand objects
        # The sort puts all the RegexCommand objects at the back, making them
        # be matched last

        return sorted(self._filter_attrs(lambda val: isinstance(val, Command)),
                      key=lambda x: isinstance(x, RegexCommand))

    @cached_property
    def daemons(self) -> List[Daemon]:
        return self._filter_attrs(lambda val: isinstance(val, Daemon))

    @cached_property
    def default(self) -> Default:
        return next(iter(self._filter_attrs(
            lambda val: isinstance(val, Default))), None)
