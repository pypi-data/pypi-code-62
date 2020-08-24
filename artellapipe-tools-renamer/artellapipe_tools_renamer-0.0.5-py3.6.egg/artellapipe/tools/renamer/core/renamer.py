#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool to rename DCC objects in an easy way
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

from artellapipe.core import tool

# Defines ID of the tool
TOOL_ID = 'artellapipe-tools-renamer'

import tpDcc
import artellapipe
from tpDcc.tools.renamer.core import model, view, controller


class RenamerTool(tool.ArtellaTool, object):
    def __init__(self, *args, **kwargs):
        super(RenamerTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.ArtellaTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Renamer',
            'id': 'artellapipe-tools-renamer',
            'logo': 'renamer_logo',
            'icon': 'renamer',
            'tooltip': 'Tool to rename DCC objects in an easy way',
            'tags': ['renamer', 'dcc'],
            'sentry_id': 'https://0e351be2ec4d4360980db9b85980e176@sentry.io/1864142',
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Renamer', 'load_on_startup': False, 'color': '', 'background_color': ''},
            'menu': [
                {'label': 'General',
                 'type': 'menu', 'children': [{'id': 'artellapipe-tools-renamer', 'type': 'tool'}]}],
            'shelf': [
                {'name': 'General',
                 'children': [{'id': 'artellapipe-tools-renamer', 'display_label': False, 'type': 'tool'}]}
            ]
        }
        base_tool_config.update(tool_config)

        return base_tool_config


class RenamerToolset(tool.ArtellaToolset, object):
    ID = TOOL_ID

    def __init__(self, *args, **kwargs):
        super(RenamerToolset, self).__init__(*args, **kwargs)

    def contents(self):

        renamer_config = tpDcc.ConfigsMgr().get_config('tpDcc-tools-renamer')
        renamer_config.data.update(self._config.data)

        naming_config = tpDcc.ConfigsMgr().get_config(
            config_name='tpDcc-naming',
            package_name=artellapipe.project.get_clean_name(),
            root_package_name='tpDcc',
            environment=artellapipe.project.get_environment()
        )
        naming_lib = artellapipe.NamesMgr().naming_lib

        renamer_model = model.RenamerModel(
            config=renamer_config, naming_config=naming_config, naming_lib=naming_lib)
        renamer_controller = controller.RenamerController(client=self._client, model=renamer_model)
        renamer_view = view.RenamerView(
            model=renamer_model, controller=renamer_controller, parent=self)

        return [renamer_view]
