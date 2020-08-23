## Copyright (c) 2020 mangalbhaskar
"""Caution: recursive utility functions."""
__author__ = 'mangalbhaskar'

import os

def dict_keys_to_lowercase(d):
  """Converts all the dictionary keys to lowercase in
  recursive function call.
  """
  d_mod = { k.lower():d[k] if not isinstance(d[k],dict) else dict_keys_to_lowercase(d[k]) for k in d.keys() }
  return d_mod

def get_from_dict(dictionary, keys=None):
  """recursive generator to fetch the non-dict values in the nested dictory.

  References:
  * https://stackoverflow.com/questions/38254304/can-generators-be-recursive
  """
  if not keys:
    keys = list(dictionary.keys())
  for val in keys:
    vval = dictionary[val]
    if type(vval) != dict:
      yield val, vval
    if type(vval) == dict:
      yield from get_from_dict(vval)

def get_basepath(path):
  """Ensures the last Directory of a path in a consistent ways.
  basepath is returned for a file or path. It takes care of
  trailing slash for a file or a directory.
  """
  if os.path.isdir(path):
    base_path = os.path.join(path,'')
  else:
    base_path = os.path.join(os.path.dirname(path),'')
  _bp = base_path.rstrip(os.path.sep)
  if os.path.isfile(_bp):
    _bp = get_basepath(_bp)
  return _bp
