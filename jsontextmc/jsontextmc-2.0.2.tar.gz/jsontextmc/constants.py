#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constant variables like version numbers."""
PROJECT: str = "JSONTextMC"
VERSION: str = "2.0.2"
DESCRIPTION: str = "JSONTextMC converts legacy color codes to the modern JSON format."
LONG_DOC: str = """Translate format-text to list, using ``sep`` as the format code separator.

To use 1.16 hex colors, use ``&#RRGGBB``, where R, G, B are red, green, blue, respectively.

If strict mode is on:
  * codes inherited from previous entries in the string will not carry over
  * formatting will not work after a color char
  * color will not work after a formatting char
If you have issues with not being able to combine character codes, turn ``strict`` off."""
