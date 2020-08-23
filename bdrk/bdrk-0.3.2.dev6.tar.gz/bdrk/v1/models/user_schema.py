# coding: utf-8

"""
    Bedrock

    API documentation for Bedrock platform  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class UserSchema(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict):       The key is attribute name
                                  and the value is attribute type.
      attribute_map (dict):       The key is attribute name
                                  and the value is json key in definition.
      readonly_attributes (dict): Set of readonly attributes (will not be
                                  serialised in request body).
    """
    openapi_types = {
        'email_address': 'str',
        'entity_id': 'str',
        'object': 'str',
        'user_name': 'str'
    }

    attribute_map = {
        'email_address': 'email_address',
        'entity_id': 'entity_id',
        'object': 'object',
        'user_name': 'user_name'
    }

    readonly_attributes = {
        'entity_id',
        'object',
        'user_name'
    }

    def __init__(self, email_address=None, entity_id=None, object='user', user_name=None, **kwargs):  # noqa: E501
        """UserSchema - a model defined in OpenAPI"""  # noqa: E501

        self._email_address = None
        self._entity_id = None
        self._object = None
        self._user_name = None
        self.discriminator = None

        self.email_address = email_address

    @classmethod
    def from_response(cls, email_address=None, entity_id=None, object='user', user_name=None, **kwargs):  # noqa: E501
        """Instantiate UserSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._email_address = None
        self._entity_id = None
        self._object = None
        self._user_name = None
        self.discriminator = None

        self.email_address = email_address
        if entity_id is not None:
            self.entity_id = entity_id
        if object is not None:
            self.object = object
        if user_name is not None:
            self.user_name = user_name
        return self

    @property
    def email_address(self):
        """Gets the email_address of this UserSchema.  # noqa: E501


        :return: The email_address of this UserSchema.  # noqa: E501
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """Sets the email_address of this UserSchema.


        :param email_address: The email_address of this UserSchema.  # noqa: E501
        :type: str
        """
        if email_address is None:
            raise ValueError("Invalid value for `email_address`, must not be `None`")  # noqa: E501

        self._email_address = email_address

    @property
    def entity_id(self):
        """Gets the entity_id of this UserSchema.  # noqa: E501


        :return: The entity_id of this UserSchema.  # noqa: E501
        :rtype: str
        """
        return self._entity_id

    @entity_id.setter
    def entity_id(self, entity_id):
        """Sets the entity_id of this UserSchema.


        :param entity_id: The entity_id of this UserSchema.  # noqa: E501
        :type: str
        """

        self._entity_id = entity_id

    @property
    def object(self):
        """Gets the object of this UserSchema.  # noqa: E501


        :return: The object of this UserSchema.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this UserSchema.


        :param object: The object of this UserSchema.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def user_name(self):
        """Gets the user_name of this UserSchema.  # noqa: E501


        :return: The user_name of this UserSchema.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this UserSchema.


        :param user_name: The user_name of this UserSchema.  # noqa: E501
        :type: str
        """

        self._user_name = user_name

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
        if not isinstance(other, UserSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
