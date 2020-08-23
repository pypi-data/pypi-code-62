__version__ = '0.4.1'

from . import commands as cmds

commands = {
    name : func
    for name, func in cmds.__dict__.items()
    if not name.startswith('_')
}
