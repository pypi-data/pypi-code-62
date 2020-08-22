# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulpcore.configuration import Configuration


class PermissionResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_href': 'object',
        'id': 'object',
        'permission': 'str',
        'obj': 'str'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'id': 'id',
        'permission': 'permission',
        'obj': 'obj'
    }

    def __init__(self, pulp_href=None, id=None, permission=None, obj=None, local_vars_configuration=None):  # noqa: E501
        """PermissionResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._id = None
        self._permission = None
        self._obj = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if id is not None:
            self.id = id
        if permission is not None:
            self.permission = permission
        if obj is not None:
            self.obj = obj

    @property
    def pulp_href(self):
        """Gets the pulp_href of this PermissionResponse.  # noqa: E501


        :return: The pulp_href of this PermissionResponse.  # noqa: E501
        :rtype: object
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this PermissionResponse.


        :param pulp_href: The pulp_href of this PermissionResponse.  # noqa: E501
        :type: object
        """

        self._pulp_href = pulp_href

    @property
    def id(self):
        """Gets the id of this PermissionResponse.  # noqa: E501


        :return: The id of this PermissionResponse.  # noqa: E501
        :rtype: object
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PermissionResponse.


        :param id: The id of this PermissionResponse.  # noqa: E501
        :type: object
        """

        self._id = id

    @property
    def permission(self):
        """Gets the permission of this PermissionResponse.  # noqa: E501


        :return: The permission of this PermissionResponse.  # noqa: E501
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """Sets the permission of this PermissionResponse.


        :param permission: The permission of this PermissionResponse.  # noqa: E501
        :type: str
        """

        self._permission = permission

    @property
    def obj(self):
        """Gets the obj of this PermissionResponse.  # noqa: E501

        Content object.  # noqa: E501

        :return: The obj of this PermissionResponse.  # noqa: E501
        :rtype: str
        """
        return self._obj

    @obj.setter
    def obj(self, obj):
        """Sets the obj of this PermissionResponse.

        Content object.  # noqa: E501

        :param obj: The obj of this PermissionResponse.  # noqa: E501
        :type: str
        """

        self._obj = obj

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PermissionResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PermissionResponse):
            return True

        return self.to_dict() != other.to_dict()
