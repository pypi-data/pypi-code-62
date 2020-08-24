#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Plot Twist nomenclature validator implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import pyblish.api

import tpDcc as tp

import artellapipe


class SelectInvalidNodes(pyblish.api.Action):
    label = 'Select Nodes with Invalid names'
    on = 'failed'

    def process(self, context, plugin):

        for instance in context:
            if not instance.data['publish'] or not instance.data['_has_failed']:
                continue

            node = instance.data.get('node', None)
            assert node and tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)

            invalid_nodes = instance.data.get('invalid_nodes')
            if not invalid_nodes:
                continue

            tp.Dcc.select_object(invalid_nodes)


class ValidatePlotTwistModelingNomenclature(pyblish.api.InstancePlugin):
    """
    Checks if modeling file has a valid nomenclature
    """

    label = 'General - Check Geometry Nomenclature'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    optional = False
    actions = [SelectInvalidNodes]

    def process(self, instance):
        assert tp.is_maya(), 'Check Modeling Nomenclature is only available in Maya!'

        node = instance.data.get('node', None)
        assert tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)

        nodes_to_check = self._nodes_to_check(node)
        assert nodes_to_check, 'No Nodes to check found!'

        invalid_nodes = list()

        for node in nodes_to_check:
            valid_name = artellapipe.NamesMgr().check_node_name(node)
            if not valid_name:
                invalid_nodes.append(node)

        instance.data['invalid_nodes'] = invalid_nodes

        assert not invalid_nodes, 'Nodes with invalid names found: {}'.format(invalid_nodes)

    def _nodes_to_check(self, node):
        nodes = tp.Dcc.list_children(node=node, all_hierarchy=True, full_path=True, children_type='transform')
        if not nodes:
            nodes = [node]
        else:
            nodes.append(node)

        return nodes


class ValidatePlotTwistProxyMeshNomenclature(pyblish.api.InstancePlugin):
    """
    Checks if proxy mesh has valid nomenclature
    """

    label = 'General - Check Proxy Nomenclature'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['proxy']
    optional = False

    def process(self, instance):
        assert tp.is_maya(), 'Validate Proxy Mesh Nomenclature is only available in Maya!'

        node = instance.data.get('node', None)
        assert tp.Dcc.object_exists(node), 'No valid proxy mesh node found in current instance: {}'.format(instance)

        name_lib = artellapipe.NamesMgr().naming_lib
        name_lib.set_active_rule('proxy_geo')

        parsed_name = name_lib.parse(node)

        valid_name = True
        for k, v in parsed_name.items():
            if v is None:
                valid_name = False
                break

        assert valid_name, 'Proxy Mesh Node is not valid!'
