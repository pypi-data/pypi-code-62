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


class SplitPptxPresentationResult(object):
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
        'result_presentations': 'list[PresentationResult]',
        'successful': 'bool'
    }

    attribute_map = {
        'result_presentations': 'ResultPresentations',
        'successful': 'Successful'
    }

    def __init__(self, result_presentations=None, successful=None):  # noqa: E501
        """SplitPptxPresentationResult - a model defined in Swagger"""  # noqa: E501

        self._result_presentations = None
        self._successful = None
        self.discriminator = None

        if result_presentations is not None:
            self.result_presentations = result_presentations
        if successful is not None:
            self.successful = successful

    @property
    def result_presentations(self):
        """Gets the result_presentations of this SplitPptxPresentationResult.  # noqa: E501


        :return: The result_presentations of this SplitPptxPresentationResult.  # noqa: E501
        :rtype: list[PresentationResult]
        """
        return self._result_presentations

    @result_presentations.setter
    def result_presentations(self, result_presentations):
        """Sets the result_presentations of this SplitPptxPresentationResult.


        :param result_presentations: The result_presentations of this SplitPptxPresentationResult.  # noqa: E501
        :type: list[PresentationResult]
        """

        self._result_presentations = result_presentations

    @property
    def successful(self):
        """Gets the successful of this SplitPptxPresentationResult.  # noqa: E501

        True if the operation was successful, false otherwise  # noqa: E501

        :return: The successful of this SplitPptxPresentationResult.  # noqa: E501
        :rtype: bool
        """
        return self._successful

    @successful.setter
    def successful(self, successful):
        """Sets the successful of this SplitPptxPresentationResult.

        True if the operation was successful, false otherwise  # noqa: E501

        :param successful: The successful of this SplitPptxPresentationResult.  # noqa: E501
        :type: bool
        """

        self._successful = successful

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
        if issubclass(SplitPptxPresentationResult, dict):
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
        if not isinstance(other, SplitPptxPresentationResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
