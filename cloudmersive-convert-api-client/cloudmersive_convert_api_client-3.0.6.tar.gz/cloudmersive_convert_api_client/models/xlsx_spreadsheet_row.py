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


class XlsxSpreadsheetRow(object):
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
        'cells': 'list[XlsxSpreadsheetCell]'
    }

    attribute_map = {
        'path': 'Path',
        'cells': 'Cells'
    }

    def __init__(self, path=None, cells=None):  # noqa: E501
        """XlsxSpreadsheetRow - a model defined in Swagger"""  # noqa: E501

        self._path = None
        self._cells = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if cells is not None:
            self.cells = cells

    @property
    def path(self):
        """Gets the path of this XlsxSpreadsheetRow.  # noqa: E501

        The Path of the location of this object; leave blank for new rows  # noqa: E501

        :return: The path of this XlsxSpreadsheetRow.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this XlsxSpreadsheetRow.

        The Path of the location of this object; leave blank for new rows  # noqa: E501

        :param path: The path of this XlsxSpreadsheetRow.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def cells(self):
        """Gets the cells of this XlsxSpreadsheetRow.  # noqa: E501

        Spreadsheet Cells in the spreadsheet row  # noqa: E501

        :return: The cells of this XlsxSpreadsheetRow.  # noqa: E501
        :rtype: list[XlsxSpreadsheetCell]
        """
        return self._cells

    @cells.setter
    def cells(self, cells):
        """Sets the cells of this XlsxSpreadsheetRow.

        Spreadsheet Cells in the spreadsheet row  # noqa: E501

        :param cells: The cells of this XlsxSpreadsheetRow.  # noqa: E501
        :type: list[XlsxSpreadsheetCell]
        """

        self._cells = cells

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
        if issubclass(XlsxSpreadsheetRow, dict):
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
        if not isinstance(other, XlsxSpreadsheetRow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
