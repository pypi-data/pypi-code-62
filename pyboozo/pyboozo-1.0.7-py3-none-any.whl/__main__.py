## Copyright (c) 2020 mangalbhaskar.
"""
Create the required project structure and the environment configurations.
"""
__author__ = 'mangalbhaskar'

import logging
import logging.config
import os
import pathlib
import shutil
import sys

import click

this = sys.modules[__name__]
this_dir = os.path.dirname(__file__)

from .config._log_ import logcfg
log = logging.getLogger('__main__.'+__name__)
logging.config.dictConfig(logcfg)

from .config import bootstrap
from .config.env import EnvCfgo
from .utils import snek
from .utils import color


default_root = os.path.join(os.getcwd(), "{}-{}".format(os.path.basename(this_dir), 'hub'))
clear = lambda: os.system('clear')

def echo():
  log.debug("__main__.py")
  pass


clear()

@click.command()
@click.option('--name', prompt=color.text('Application name', cc=color.on_cya),
              default='boozo',
              help='Name of the main application; max: 7 chars [a-z]')
@click.option('--root', prompt=color.text('Root directory for application', cc=color.on_cya),
              default=default_root,
              help='Absolute path for application Root directory. Defaults to current directory.')
@click.option('--prefix', prompt=color.text('Prefix for environment variables', cc=color.on_cya),
              default='BZO',
              help='Prefix ensures the unique namespace; max: 3 [a-z] chars')
@click.option('--timestamp',
              is_flag=True,
              help='Easier to create multiple directories and switch between if used along with softlink')
@click.option('--gitkeep',
              is_flag=True,
              help='Create the empty hidden file (.gitkeep) in each directory')
def main(root, name, prefix, timestamp, gitkeep):
  """
  Create the directories, smylinks and the configuration files.
  """
  try:
    echo()
    ## main home paths
    __envars = {}
    __envars['_NAME'] = name
    __envars['_PREFIX'] = prefix
    __envars['_ROOT'] = root
    __envars['_IS_TIMESTAMP_DATA_DIR'] = timestamp

    envcfgo = EnvCfgo(__envars)

    _dirpaths = [envcfgo._CONFIG_ROOT]+ \
      envcfgo._DIR_PATH+envcfgo._DATA_DIR_PATH+envcfgo._MOBILE_DIR_PATH+ \
      [envcfgo._VMHOME, envcfgo._PYVENV_PATH]

    color.cprint("Creating setup...")
    bootstrap.make_dirs(*_dirpaths, gitkeep=gitkeep)

    gitignore_filepath = os.path.join(envcfgo._HOME,'.gitignore')
    if not os.path.isfile(gitignore_filepath):
      ## copy pre-configured gitignore template, if it does not exists to prevent overriding customized file
      shutil.copy(os.path.join(this_dir,'data','gitignore'), gitignore_filepath)

    if envcfgo._IS_TIMESTAMP_DATA_DIR:
      bootstrap.make_links(*envcfgo._DATA_DIR_PATH)

    bootstrap.make_links(**envcfgo._LINK)

    kwargs = envcfgo.get_kwargs()
    log.debug("kwargs: {}".format(kwargs))

    bootstrap.generate_cfgyml(**kwargs)
    bootstrap.generate_exportsh(**kwargs)
    bootstrap.generate_aliassh(**kwargs)
    env_filepath = bootstrap.generate_envsh(**kwargs)

    color.cprint("Hurrayy!!! Project structure Initialized!", cc=color.bired)
    color.cprint("Shape the Future - Code, Eat, Sleep & Repeat.\n", cc=color.biyel)
    color.cprint("Project Root: ", cc=color.bpur, es=root)
    color.cprint("Main application directory: ", cc=color.bpur, es=os.path.join(root, name))

    color.cprint(snek.fancy)
    color.cprint("Put this in file: ", cc=color.biyel, es="~/.bashrc")
    color.cprint("source {}\n".format(env_filepath), cc=color.bblu)
  except:
    import traceback
    traceback.print_exception(*sys.exc_info()) 

if __name__ == "__main__":
  main()

