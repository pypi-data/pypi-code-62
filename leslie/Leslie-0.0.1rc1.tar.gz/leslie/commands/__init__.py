# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: __init__.py
@time: 2019/12/11 14:48

这一行开始写关于本文件的说明与解释


"""
import argparse
from leslie import __version__
from typing import Any, Optional
from overrides import overrides

from leslie.commands.subcommand import Subcommand


class ArgumentParser(argparse.ArgumentParser):
    """
        Custom argument parser that will display the default value for an argument
        in the help message.
        """

    _action_defaults_to_ignore = {"help"}

    @staticmethod
    def _is_empty_default(default: Any) -> bool:
        if default is None:
            return True
        if isinstance(default, (str, list, tuple, set)):
            return not bool(default)
        return False

    @overrides
    def add_argument(self, *args, **kwargs):
        # Add default value to the help message when the default is meaningful.
        default = kwargs.get("default")
        if kwargs.get(
                "action"
        ) not in self._action_defaults_to_ignore and not self._is_empty_default(default):
            description = kwargs.get("help", "")
            kwargs["help"] = f"{description} (default = {default})"
        super().add_argument(*args, **kwargs)


def create_parser(program):
    """
        Creates the argument parser for the main program.
        """
    parser = ArgumentParser(description="Run Leslie", prog=program)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(title="Commands", metavar="")
    for subcommand_name in sorted(Subcommand.list_available()):
        subcommand_class = Subcommand.by_name(subcommand_name)
        subcommand = subcommand_class()
        subparser = subcommand.add_subparser(subparsers)
        subparser.add_argument(
            "--include-package",
            type=str,
            action="append",
            default=[],
            help="additional packages to include",
        )

    return parser


def main(program):
    parser = create_parser(program)
    args = parser.parse_args()
    if "func" in dir(args):
        args.func(args)
    else:
        parser.print_help()
