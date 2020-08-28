import abc
import os
import types

import appdirs

from .. import info


class Vars(metaclass=abc.ABCMeta):
    def attach_parser(self, parser):
        for k, v in self._dict().items():
            if isinstance(v, (list, set)):
                parser.add_argument(f'--{k}', nargs='+',
                                    help=getattr(self, f'_{k}_help'))
            else:
                parser.add_argument(f'--{k}', type=type(v),
                                    help=getattr(self, f'_{k}_help'))

    def apply(self, args):
        for k in self._keys():
            v = getattr(args, k)
            if v is None:
                continue
            if isinstance(getattr(self, k), set):
                v = set(v)
            setattr(self, k, v)

    def _keys(self):
        return [k for k in dir(self) if
                not k.startswith('_') and
                not isinstance(getattr(self, k), types.MethodType)]

    def _dict(self):
        return {k: getattr(self, k) for k in self._keys()}

    def __repr__(self):
        return repr(self._dict())


class EnvVars(Vars):
    root = appdirs.user_data_dir(info.APP_NAME, info.APP_AUTHOR)
    _root_help = 'hehehehe'  # TODO: to be implemented

    devices = set()
    _devices_help = 'hehehehe'  # TODO: to be implemented

    def __init__(self):
        super().__init__()
        self._load_env()

    def _load_env(self):
        for key_origin in self._keys():
            key = f'N3_{key_origin.upper()}'
            if key in os.environ:
                value = os.environ[key]
                origin = getattr(self, key_origin)

                if isinstance(origin, (list, set)):
                    value = [v.strip() for v in value.split(',')]
                    if isinstance(origin, set):
                        value = set(value)
                else:
                    raise Exception(
                        f'unexpected type for "{key_origin}": "{type(origin).__name__}"')
                setattr(self, key_origin, value)
