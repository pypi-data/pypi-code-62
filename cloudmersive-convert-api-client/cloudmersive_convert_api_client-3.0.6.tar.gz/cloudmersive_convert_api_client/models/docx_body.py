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


class DocxBody(object):
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
        'path': 'str',
        'all_paragraphs': 'list[DocxParagraph]',
        'all_tables': 'list[DocxTable]'
    }

    attribute_map = {
        'path': 'Path',
        'all_paragraphs': 'AllParagraphs',
        'all_tables': 'AllTables'
    }

    def __init__(self, path=None, all_paragraphs=None, all_tables=None):  # noqa: E501
        """DocxBody - a model defined in Swagger"""  # noqa: E501

        self._path = None
        self._all_paragraphs = None
        self._all_tables = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if all_paragraphs is not None:
            self.all_paragraphs = all_paragraphs
        if all_tables is not None:
            self.all_tables = all_tables

    @property
    def path(self):
        """Gets the path of this DocxBody.  # noqa: E501

        The Path of the location of this object; leave blank for new tables  # noqa: E501

        :return: The path of this DocxBody.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this DocxBody.

        The Path of the location of this object; leave blank for new tables  # noqa: E501

        :param path: The path of this DocxBody.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def all_paragraphs(self):
        """Gets the all_paragraphs of this DocxBody.  # noqa: E501

        All paragraphs anywhere in the document; these objects are not sequentially placed but are scatted across document  # noqa: E501

        :return: The all_paragraphs of this DocxBody.  # noqa: E501
        :rtype: list[DocxParagraph]
        """
        return self._all_paragraphs

    @all_paragraphs.setter
    def all_paragraphs(self, all_paragraphs):
        """Sets the all_paragraphs of this DocxBody.

        All paragraphs anywhere in the document; these objects are not sequentially placed but are scatted across document  # noqa: E501

        :param all_paragraphs: The all_paragraphs of this DocxBody.  # noqa: E501
        :type: list[DocxParagraph]
        """

        self._all_paragraphs = all_paragraphs

    @property
    def all_tables(self):
        """Gets the all_tables of this DocxBody.  # noqa: E501

        All tables anywhere in the document; these objects are not sequentially placed but are scatted across the document  # noqa: E501

        :return: The all_tables of this DocxBody.  # noqa: E501
        :rtype: list[DocxTable]
        """
        return self._all_tables

    @all_tables.setter
    def all_tables(self, all_tables):
        """Sets the all_tables of this DocxBody.

        All tables anywhere in the document; these objects are not sequentially placed but are scatted across the document  # noqa: E501

        :param all_tables: The all_tables of this DocxBody.  # noqa: E501
        :type: list[DocxTable]
        """

        self._all_tables = all_tables

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
        if issubclass(DocxBody, dict):
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
        if not isinstance(other, DocxBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
