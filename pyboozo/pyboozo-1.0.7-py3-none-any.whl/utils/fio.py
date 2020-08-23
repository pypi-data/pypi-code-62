## Copyright (c) 2020 mangalbhaskar
"""Common File I/O utilities.

Dependencies:
* edict, pandas, yaml
"""
__author__ = 'mangalbhaskar'

import errno
import logging
import logging.config
import os
import json
import pathlib
import sys
import time

from easydict import EasyDict as edict
import yaml

from boozo.config._log_ import logcfg
log = logging.getLogger('__main__.'+__name__)
logging.config.dictConfig(logcfg)

this = sys.modules[__name__]


def load_file(filepath, withedict=True):
  """Safe load file as easy dictionary object by default.
  Currently, `yml`, `json`, `csv` files are supported."""
  fc = None
  if str == type(filepath) and os.path.exists(filepath) and os.path.isfile(filepath):
    ext = os.path.splitext(filepath)[-1].split('.')[-1]
    log.debug("ext, type(ext): {}, {}".format(ext, type(ext)))
    fn = getattr(this, ext+'_load') 
    fc = fn(filepath, withedict)
  else:
    log.exception("Invalid filepath: {}".format(filepath), exc_info=True)
  return fc

def yml_load(filepath, withedict=True):
  """Safe load yaml file as easy dictionary object."""
  fc = None
  tic = time.time()
  log.debug("filepath, type(filepath): {}, {}".format(filepath, type(filepath)))
  with open(filepath, 'r') as f:
    if withedict:
      ## fc = edict(yaml.load(f))
      fc = edict(yaml.safe_load(f))
    else:
      fc = yaml.safe_load(f)
    log.debug('Done (t={:0.2f}s)'.format(time.time()- tic))
  return fc

def json_load(filepath, withedict=True):
  """Load json file as easy dictionary object."""
  fc = None
  tic = time.time()
  with open(filepath, 'r') as f:
    if withedict:
      fc = edict(json.load(f))
    else:
      fc = json.load(f)
    log.info('Done (t={:0.2f}s)'.format(time.time()- tic))
  return fc

def csv_load(filepath, withedict=True):
  """Load csv file as easy dictionary object."""
  import pandas as pd
  if withedict:
    fc = edict(pd.read_csv(filepath))
  else:
    fc = pd.read_csv(filepath)
  return fc

def read_csv_line(filepath, delimiter = ','):
  """Read CSV Line as a generator for large csv files."""
  with open(filepath, 'r') as f:
    gen = (i for i in f)
    ## next(gen)
    yield next(gen).rstrip('\n').split(delimiter)
    for line in gen:
      yield line.rstrip('\n').split(delimiter)

def yml_safe_dump(filepath, o, default_flow_style=False):
  """Create yaml file from python dictionary object."""
  with open(filepath,'w') as f:
    yaml.safe_dump(o, f, default_flow_style=default_flow_style)

def json_dump(filepath, o):
  """Create json file from python dictionary object."""
  tic = time.time()
  with open(filepath,'w') as f:
    f.write(json.dumps(o))
    log.info('Done (t={:0.2f}s)'.format(time.time()- tic))

def list_files(p, ext=None):
  """List files in a given path."""
  pattern = r'**/*.{}'.format(ext) if ext else r'**/*'
  for f in pathlib.Path(p).glob(pattern):
    if os.path.isfile(f):
     yield f.as_posix()

def list_dirs(p):
  """List directories in a given path."""
  for f in pathlib.Path(p).glob(r'**/*'):
    if os.path.isdir(f):
     yield f.as_posix()

def mkdir_p(path):
  """mkdir -p` linux command functionality.

  References:
  * https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
  * https://stackoverflow.com/questions/20794/find-broken-symlinks-with-python
  """
  try:
    os.makedirs(path)
  except OSError as exc:  ## Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    elif os.path.islink(path) and not os.path.exists(path):
      os.remove(path)
      mkdir_p(path)
    else:
      raise
