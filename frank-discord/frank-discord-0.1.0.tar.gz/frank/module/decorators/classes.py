# =====IMPORTS=====
# Future imports
from __future__ import annotations

# Built-in imports
import re


class Simple:
    """
    Acts as a base class for all other types; behaves like the given
    function
    """

    def __init__(self, func: callable):
        """
        Args:
            func: function to mimic
        """

        self.func = func

    def __call__(self, *args, **kwargs):
        """
        All this call does is call the wrapped function. Because we overwrote
        __get__, we can pass self to the function, making it behave as a class
        method of the instance calling it.
        """

        return self.func.__call__(self._obj, *args, **kwargs)

    def __get__(self, instance, owner) -> Simple:
        """
        We use __get__ to get the class calling the function. This allows us to
        pass 'self' to the wrapped function, effectively making this class
        fully behave as a class method.

        Args:
            instance: instance calling the function
            owner: type of the function
        """

        self._cls = owner
        self._obj = instance

        return self


class Command(Simple):
    """
    Represents a command of the module.
    """

    def __init__(self, func: callable, cmd: str, help_str: str = None):
        """
        Args:
            func: function to wrap
            cmd: keyword used to call this function
            help_str: short description of the command
        """

        super().__init__(func)

        self.cmd = cmd
        self.help_str = help_str

    def match(self, prefix: str) -> bool:
        """
        Returns wether the command matches the given prefix.

        Args:
            prefix: string to match own prefix against
        """

        return self.cmd == prefix


class RegexCommand(Command):
    """
    A subclass of Command that can use a regex pattern instead of a fixed
    prefix.
    """

    def match(self, prefix: str) -> bool:
        """
        Returns wether the regex pattern matches the given prefix.

        Args:
            prefix: string to match pattern against; Pattern must match entire
            prefix
        """

        return bool(re.fullmatch(self.cmd, prefix))


class Daemon(Simple):
    """
    Represents a daemon. Currently, it's only used as its own type, but writing
    it this way allows us to easily expand upon its functionality later.
    """

    pass


class Default(Simple):
    """
    Represents a default command (a.k.a. when the module is called without a
    command.
    """

    def __init__(self, func: callable, help_str: str = None):
        """
        Args:
            func: function to wrap
            help_str: short description of the default command
        """

        super().__init__(func)

        self.help_str = help_str
