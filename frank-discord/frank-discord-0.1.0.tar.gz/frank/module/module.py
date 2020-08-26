# =====IMPORTS=====
# Future imports
from __future__ import annotations

# Built-in imports
import asyncio

# Own imports
from .exceptions import InvalidCommand
from .meta import ModuleMeta
from .decorators import RegexCommand

# Typing imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Built-in imports
    from typing import List, Dict

    # Third-party imports
    from discord.abc import User, Messageable

    # Own imports
    from suzybot.frank import Frank


class Module(ModuleMeta):
    """
    Base class for modules; all custom modules should inherit from this.
    """

    PREFIX = []
    """
    Prefix to activate this module.
    """

    NAME = ''
    """
    The name is used in various places, such as the config file and the
    help function.
    """

    HELP = ''
    """
    Short description of the module to use in the help function.
    """

    def __init__(self, client: Frank, config: Dict = None):
        """
        Args:
            client: client using this module; used to communicate.
            config: dict containing the config for this module (Frank client
                reads this from the config file).
        """

        super().__init__()

        self._client = client
        self._config = config

        self._tasks = []

    def pre_start(self):
        """
        Overwrite this function to run code (e.g. add variables...) before
        starting the daemons.
        """

        pass

    async def _start(self):
        """Start up defined daemons for this module."""

        self.pre_start()

        for daemon in self.daemons:  # pylint: disable=no-member
            task = asyncio.create_task(daemon())
            self._tasks.append(task)

    async def stop(self):
        """
        Stop all tasks for this module.
        """

        for task in self._tasks:
            task.cancel()

    async def __call__(self, cmd: List[str], author: User,
                       channel: Messageable, mid: int):
        """
        Execute the command, if found.

        Args:
            cmd: list of command arguments; if empty, default command is used
            author: author of message
            channel: channel the message was sent in
            mid: message id
        """

        if cmd:
            func = next((func for func in self.commands
                         if func.match(cmd[0])), None)

            if func:
                # A RegexCommand can use the prefix, as it's not a fixed string
                if isinstance(func, RegexCommand):
                    await func(prefix=cmd[0], cmd=cmd[1:], author=author,
                               channel=channel, mid=mid)

                else:
                    await func(cmd=cmd[1:], author=author, channel=channel,
                               mid=mid)

            else:
                raise InvalidCommand(f'Unknown command: {cmd}')

        elif self.default:
            await self.default(author=author, channel=channel, mid=mid)

    @classmethod
    def match(cls, prefix: str) -> bool:
        """
        Checks wether the given prefix matches the module.

        Args:
            prefix: prefix to check
        """

        if cls.PREFIX:
            if isinstance(cls.PREFIX, list):
                return prefix in cls.PREFIX

            else:
                return prefix == cls.PREFIX

        else:
            return False
