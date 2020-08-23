## Copyright (c) 2020 mangalbhaskar
"""Casting utility functions.

References:
* https://github.com/joke2k/django-environ
"""
__author__ = 'mangalbhaskar'

BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')

def to_bool(value):
  try:
    value = int(value) != 0
  except (TypeError, ValueError) as e:
    value = True if value and value.lower() in BOOLEAN_TRUE_STRINGS else False
  return value
