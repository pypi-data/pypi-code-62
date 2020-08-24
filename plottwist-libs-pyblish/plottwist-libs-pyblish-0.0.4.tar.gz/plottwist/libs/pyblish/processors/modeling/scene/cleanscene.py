#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains clean scene processor implementation for Plot Twist
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"


import pyblish.api


class RemoveUnusedReferences(pyblish.api.ContextPlugin):
    """
    Forces the cleanup of unused reference nodes
    """

    label = 'Scene - Remove Unused References'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):

        import tpDcc.dccs.maya as maya

        maya.mel.eval('RNdeleteUnused')

        return True


class RemoveUnusedDeformers(pyblish.api.ContextPlugin):
    """
    Forces the cleanup of unused reference nodes
    """

    label = 'Scene - Remove Unused Deformers'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False

    def process(self, context):

        import tpDcc.dccs.maya as maya

        maya.mel.eval('deleteUnusedDeformers')

        return True
