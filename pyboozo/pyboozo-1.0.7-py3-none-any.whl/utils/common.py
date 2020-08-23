## Copyright (c) 2020 mangalbhaskar
"""Commonly utility functions."""
__author__ = 'mangalbhaskar'

import logging
import logging.config
import os
import re
import sys

from boozo.config._log_ import logcfg
log = logging.getLogger('__main__.'+__name__)
logging.config.dictConfig(logcfg)

def str_to_list(word, dl=','):
  """Converts a string to a list for the given delimiter."""
  regexp = re.compile(r'['+dl+']')
  if regexp.search(word):
    x = word.split(',')
    x = [i.strip() for i in x if i.strip() ]
  else:
    x = [word]
  return x


def list_to_str(l, dl='_', quote=False):
  """Convert a list to string for the given delimeter."""
  if quote:
    r = dl.join(["'"+str(i).lower()+"'" for i in l if i is not None and str(i).strip()])
  else:
    r = dl.join([str(i).lower() for i in l if i is not None and str(i).strip()])
  return r


def camel_to_snake(s):
  """Convert `CamelCase` to the `snake_case`.

  Credits:
  * https://stackoverflow.com/users/1522117
  * https://stackoverflow.com/users/3423324/luckydonald

  References:
  * https://stackoverflow.com/a/12867228
  """
  a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))')
  return a.sub(r'_\1', s).lower()


def snake_to_camel(s):
  """Convert `snake_case` to the `CamelCase`.

  Credits:
  * https://stackoverflow.com/users/129879

  References:
  * https://stackoverflow.com/a/1176023
  * https://www.w3resource.com/python-exercises/re/python-re-exercise-37.php
  """
  # return ''.join(x.capitalize() or '_' for x in s.split('_')) ## preserves the '_'
  return ''.join(x.title() for x in s.split('_'))
