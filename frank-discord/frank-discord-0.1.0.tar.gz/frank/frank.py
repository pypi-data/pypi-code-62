# =====IMPORTS=====
# Future imports
from __future__ import annotations

# Built-in imports
import shlex

# Third-party imports
import yaml
import discord

# Typing imports
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    # Own imports
    from .module import Module
    from discord import Message


class Frank(discord.Client):
    """
    Main class of the bot; works by adding modules, which all define
    their own behavior.
    """

    def __init__(self, modules: List[Module], config_file: str = 'frank.yaml',
                 prefix: str = 'fr'):
        """
        Args:
            modules: modules to load
            config_file: path to yaml config file; ignored if non-existent
            prefix: prefix to activate Frank in the Discord server
        """

        super().__init__()
        self._modules = modules
        self._loaded_modules = []

        self.PREFIX = prefix

        try:
            with open(config_file, 'r') as f:
                self._config = yaml.load(f, Loader=yaml.FullLoader)

        except FileNotFoundError:
            self._config = None

    async def on_ready(self):
        """
        Runs when the bot has succesfully connected to Discord
        """

        print('Connected')

        # Startup all modules
        for module in self._modules:
            if self._config and module.NAME in self._config:
                loaded = module(self, config=self._config[module.NAME])

            else:
                loaded = module(self)

            await loaded._start()
            self._loaded_modules.append(loaded)

        print('All modules loaded')

    async def stop(self):
        """
        Stop all module daemons and exit.
        """

        for module in self._loaded_modules:
            await module.stop()

    async def on_message(self, message: Message):
        """
        Runs when a new message is sent in the Discord channel.

        Args:
            message: object representing the received message; see
            https://discordpy.readthedocs.io/en/latest/api.html#message
        """

        try:
            cmd = shlex.split(message.content.strip())

        except ValueError:
            return

        if cmd and cmd[0] == self.PREFIX:
            module = next((mod for mod in self._loaded_modules
                           if mod.match(cmd[1])), None)

            if module:
                await module(cmd=cmd[2:], author=message.author,
                             channel=message.channel, mid=message.id)
