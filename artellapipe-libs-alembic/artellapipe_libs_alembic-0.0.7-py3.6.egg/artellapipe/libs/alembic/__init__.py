#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for artellapipe-libs-alembic
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging

import tpDcc as tp

import artellapipe.register

LOGGER = logging.getLogger('artellapipe-libs-alembic')


def init(*args, **kwargs):
    LOGGER.info('Initializing Alembic libraries ...')

    try:
        from artellapipe.libs.alembic.core import alembic
        artellapipe.register.register_class('Alembic', alembic.AbstractAlembic)

        if tp.is_maya():
            from artellapipe.libs.alembic.maya import alembic as maya_alembic
            artellapipe.register.register_class('Alembic', maya_alembic.MayaAlembic)
        elif tp.is_houdini():
            from artellapipe.libs.alembic.houdini import alembic as houdini_alembic
            artellapipe.register.register_class('Alembic', houdini_alembic.HoudiniAlembic)
    except Exception as exc:
        LOGGER.warning('Error while initializing Alembic libraries: {}!'.format(exc))
        return

    LOGGER.info('Alembic libraries initialized successfully!')
