# coding: utf-8

"""
    convertapi

    Convert API lets you effortlessly convert file formats and types.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class UpdateDocxTableRowResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'successful': 'bool',
        'edited_document_url': 'str'
    }

    attribute_map = {
        'successful': 'Successful',
        'edited_document_url': 'EditedDocumentURL'
    }

    def __init__(self, successful=None, edited_document_url=None):  # noqa: E501
        """UpdateDocxTableRowResponse - a model defined in Swagger"""  # noqa: E501

        self._successful = None
        self._edited_document_url = None
        self.discriminator = None

        if successful is not None:
            self.successful = successful
        if edited_document_url is not None:
            self.edited_document_url = edited_document_url

    @property
    def successful(self):
        """Gets the successful of this UpdateDocxTableRowResponse.  # noqa: E501

        True if successful, false otherwise  # noqa: E501

        :return: The successful of this UpdateDocxTableRowResponse.  # noqa: E501
        :rtype: bool
        """
        return self._successful

    @successful.setter
    def successful(self, successful):
        """Sets the successful of this UpdateDocxTableRowResponse.

        True if successful, false otherwise  # noqa: E501

        :param successful: The successful of this UpdateDocxTableRowResponse.  # noqa: E501
        :type: bool
        """

        self._successful = successful

    @property
    def edited_document_url(self):
        """Gets the edited_document_url of this UpdateDocxTableRowResponse.  # noqa: E501

        URL to the edited DOCX file; file is stored in an in-memory cache and will be deleted.  Call Finish-Editing to get the result document contents.  # noqa: E501

        :return: The edited_document_url of this UpdateDocxTableRowResponse.  # noqa: E501
        :rtype: str
        """
        return self._edited_document_url

    @edited_document_url.setter
    def edited_document_url(self, edited_document_url):
        """Sets the edited_document_url of this UpdateDocxTableRowResponse.

        URL to the edited DOCX file; file is stored in an in-memory cache and will be deleted.  Call Finish-Editing to get the result document contents.  # noqa: E501

        :param edited_document_url: The edited_document_url of this UpdateDocxTableRowResponse.  # noqa: E501
        :type: str
        """

        self._edited_document_url = edited_document_url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(UpdateDocxTableRowResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateDocxTableRowResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
