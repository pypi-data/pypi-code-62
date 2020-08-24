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

import maya.cmds as cmds        # Do not remove


def init():

    print('=' * 100)
    print('| Plot Twist ArtellaPipe | > Loading Plot Twist Tools')

    try:
        # Initialize tpDcc library
        import tpDcc.loader
        print(tpDcc.loader)
        tpDcc.loader.init(dev=False)

        # Initialize artellapipe library
        import artellapipe.loader
        artellapipe.loader.init(dev=False)

        # Initialize plottwist project
        import plottwist.loader
        plottwist.loader.init(dev=False)

        print('| Plot Twist Pipeline | Plot Twist loaded successfully!')
        print('=' * 100)
    except Exception as exc:
        import traceback
        print('ERROR: Impossible to load Plot Twist Tools, contact TD!')
        print('{} | {}'.format(exc, traceback.format_exc()))


# We must launch it with low priority, otherwise USD plugin loading operations will fail
cmds.evalDeferred(init, lp=True)
