#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Standalone plugin specific implementation
"""

from __future__ import print_function, division, absolute_import

from artella import register
from artella.core import dccplugin
from artella.core.utils import Singleton


class ArtellaStandalonePlugin(dccplugin.ArtellaDccPlugin, object):

    def init(self, dev=False, show_dialogs=True, create_menu=True, create_callbacks=True, *args, **kwargs):
        """
        Initializes Artella DCC plugin

        :param bool dev: Whether plugin is initialized in development mode or not
        :param bool show_dialogs: Whether dialogs should appear during plugin initialization or not
        :param bool create_menu: Whether menu should be created or not
        :param bool create_callbacks: Whether or not DCC callbacks should be created
        :return: True if the initialization was successful; False otherwise.
        :rtype: bool
        """

        super(ArtellaStandalonePlugin, self).init(dev=dev, show_dialogs=show_dialogs)


@Singleton
class ArtellaStandalonePluginSingleton(ArtellaStandalonePlugin, object):
    def __init__(self, artella_drive_client=None):
        ArtellaStandalonePlugin.__init__(self, artella_drive_client=artella_drive_client)


register.register_class('DccPlugin', ArtellaStandalonePluginSingleton)
