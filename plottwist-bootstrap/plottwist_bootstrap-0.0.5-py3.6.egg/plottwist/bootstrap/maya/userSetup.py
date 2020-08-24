#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization for Plot Twist Tools
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

print('=' * 100)
print('| Plot Twist ArtellaPipe | > Loading Plot Twist Tools')

try:
    import plottwist.loader
    from maya import cmds
    cmds.evalDeferred('plottwist.loader.init(import_libs=True)')
    print('| Plot Twist ArtellaPipe | Plot Twist loaded successfully!')
    print('=' * 100)
except Exception as e:
    try:
        dev = False

        # Initialize tpDcc library
        import tpDcc.loader
        tpDcc.loader.init(dev=dev)

        # Initialize artellapipe library
        import artellapipe.loader
        artellapipe.loader.init(dev=dev)

        # Initialize plottwist project
        import plottwist.loader
        plottwist.loader.init(dev=dev)

        print('| Plot Twist Pipeline | Plot Twist loaded successfully!')
        print('=' * 100)
    except Exception as exc:
        import traceback
        print('ERROR: Impossible to load Plot Twist Tools, contact TD!')
        print('{} | {}'.format(exc, traceback.format_exc()))
