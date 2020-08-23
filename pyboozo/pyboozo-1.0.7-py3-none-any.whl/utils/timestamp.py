## Copyright (c) 2020 mangalbhaskar
"""Common date and timestamp utilities and inter-conversion of them.

Dependencies:
* `arrow` for timezone and timestamp handling.

References:
* http://zetcode.com/python/arrow/  
"""
__author__ = 'mangalbhaskar'

import logging
import logging.config
import os

import arrow

from boozo.config._log_ import logcfg
log = logging.getLogger('__main__.'+__name__)
logging.config.dictConfig(logcfg)

from .typeformats import *


def now():
  """returns the date with timezone in consistent way.
  This to be used specifically when creating serializable objects with dates to store in the database in particular.
  """
  now = arrow.now()
  date_time_zone = now.format(_date_format_)
  return date_time_zone

def ts():
  """returns the timestamp in the `_timestamp_format_` format"""
  import datetime
  ts = (_timestamp_format_).format(datetime.datetime.now())
  return ts

def modified_on(filepath, ts=False):
  """returns the last modified timestamp with timezone.
  
  References:
  * https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
  """
  modified_on = arrow.Arrow.fromtimestamp(os.stat(filepath).st_mtime).format(_date_format_)
  if ts:
    modified_on = ts_from_datestring(modified_on)
  return modified_on

def date_from_ts(ts):
  """returns the date object from the given string date in the `_date_format_`

  Todo:
  some warning to the call to get function for api change in the future release
  """
  ar = arrow.get(ts, _date_format_)
  dt = ar.date()
  return dt

def ts_from_datestring(dt):
  """returns the timestamp in the `_timestamp_format_` given the date string in the `_date_format_` format

  Todo:
  some warning to the call to get function for api change in the future release
  """
  ar = arrow.get(dt, _date_format_)
  ts = (_timestamp_format_).format(ar.datetime)
  return ts
