from importlib.metadata import version

from justnow.parser import EventParser, get_elapse_datetime  # noqa

try:
    __version__ = version("justnow")
except ImportError:
    pass
