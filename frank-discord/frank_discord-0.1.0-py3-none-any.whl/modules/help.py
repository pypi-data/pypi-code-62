# =====IMPORTS=====
# Future imports
from __future__ import annotations

# Third-party imports
from discord import Embed

# Own imports
from .. import Module, default, regex_command

# Typing imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Built-in imports
    from typing import List

    # Third-party imports
    from discord.abc import User, Messageable


class HelpMod(Module):
    """
    This module sends a help message in a given channel with info about all
    other modules.
    """

    PREFIX = 'help'
    NAME = 'help'
    HELP = 'Shows help info about all modules'

    @default(help_str='Show help about all modules.')
    async def send_all(self, author: User, channel: Messageable, mid: int):
        embed = Embed()

        for mod in self._client._modules:
            embed.add_field(name=mod.NAME, value=mod.HELP, inline=False)

        await channel.send(embed=embed)

    @regex_command(cmd='.+', help_str='Show help about a certain module.')
    async def show_module_help(self, prefix: str, cmd: List[str], author: User,
                               channel: Messageable, mid: int):
        # Yes, this command just ignores cmd at the moment
        mod_name = prefix.lower()
        mod = next((mod for mod in self._client._modules
                    if mod.NAME.lower() == mod_name), None)

        if mod:
            embed = Embed()

            if mod.default:
                embed.add_field(name='default', value=mod.default.help_str,
                                inline=False)

            for cmd in mod._COMMANDS:
                embed.add_field(name=cmd.cmd, value=mod.help_str, inline=False)

            await channel.send(embed=embed)
