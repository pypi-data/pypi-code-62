#!/usr/env/bin python3
# -*- coding: utf-8 -*-

"""Use as script entry
"""

import sys, os
from pathlib import Path
from .utils import initGetText
from . import __version__
from ._plugin import load_scripts
availableCmds = ['gitrepo', 'monitor', 'broadcast', 'paperutil', 'wakeonlan', 'tray']

def main():
    tr = initGetText("bffacility")
    from argparse import ArgumentParser
    parser = ArgumentParser(prog='bffacility', 
        description="Usage: bffacility <subcommand> [args]")
    parser.add_argument('subcmd', type=str, nargs="?", help=tr('type sub-command to exec certain function'))
    parser.add_argument('-V', action="version", help=tr(f'show version: {__version__}'), version=f'%(prog)s {__version__}')

    args = vars(parser.parse_args(sys.argv[1:2]))
    cmd = args["subcmd"]

    sys.argv.pop(0)
    
    if cmd in availableCmds:
        arg = sys.argv[1:]
    #  add custom sub-commands here

    if cmd == 'tray':
        from .win_tray import main as tray
        tray(arg)
        return
    elif cmd == 'pri':
        pripath = Path(os.path.dirname(__file__)) / "../_pri"
        pripath = pripath.resolve()
        if len(sys.argv) < 2:
            print("Not Supported!")
            return
        try:
            subscript = sys.argv[1]
            arg = sys.argv[2:]
            load_scripts(subscript, arg, pripath)
        except Exception as e:
            print("Running: ", e) 
        return
    elif cmd in availableCmds:
        load_scripts(cmd, arg)
        return
    print(tr('Available sub commands: '))
    cmds = ""
    for i, c in enumerate(availableCmds):
        cmds += f"{i+1}: {c}  \t"
    print(cmds, "\n")
    parser.print_usage()
