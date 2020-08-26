# =====IMPORTS=====
# Own imports
from .classes import Command, RegexCommand, Daemon, Default


def command(cmd, help_str: str = None) -> callable:
    """
    Converts a method into a command by replacing it with a Command object.

    Args:
        cmd: keyword used to call this function
        help_str: short description of the command
    """

    def inner(func):
        return Command(func, cmd, help_str)

    return inner


def regex_command(pattern: str, help_str: str = None) -> callable:
    """
    Converts the method into a RegexCommand.

    Args:
        pattern: regex pattern to match command with
        help_str: short description of the command
    """

    def inner(func):
        return RegexCommand(func, pattern, help_str)

    return inner


def daemon() -> callable:
    """
    Converts the method into a Daemon, which will then be run when the module
    is started.
    """

    def inner(func):
        return Daemon(func)

    return inner


# TODO: make sure the default is unique
def default(help_str: str = None) -> callable:
    """
    Converts the method into the Default method, making it the default command
    when the module is run without a command.
    """

    def inner(func):
        return Default(func, help_str)

    return inner
