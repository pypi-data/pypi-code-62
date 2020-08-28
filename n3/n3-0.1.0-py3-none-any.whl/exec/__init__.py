import argparse
import sys
import types

from .eval import eval
from .train import train
from .variable import EnvVars


def route():
    # get the module itself, enviroment variables
    module = globals()
    env = EnvVars()

    # get the usable executions
    modes = [k for k, v in module.items()
             if isinstance(v, types.FunctionType) and v.__module__ == f'n3.exec.{k}']

    # define parser
    parser = argparse.ArgumentParser('n3',
                                     add_help=False,
                                     description='Process some integers.')
    parser.add_argument('help', type=bool, nargs='?',
                        help='show this help message and exit')
    parser.add_argument('mode', type=str, choices=modes,
                        help='hehehehe')  # TODO: add help message
    parser.add_argument('exec', type=str,
                        help='hehehehe')  # TODO: add help message

    # parser can modify envs
    env.attach_parser(parser)

    # show help message
    args = sys.argv[1:]
    if not args or len(args) == 1 and args[0] == 'help':
        parser.print_help()
        return

    # parse
    args, _ = parser.parse_known_args()
    env.apply(args)

    # execute
    module[args.mode](env, args.exec, help=args.help is True)
