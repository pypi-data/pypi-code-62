# coding: utf-8

"""
    videoapi

    The video APIs help you convert, encode, and transcode videos.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class StillFrame(object):
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
        'frame_number': 'int',
        'time_stamp': 'str',
        'content': 'str'
    }

    attribute_map = {
        'frame_number': 'FrameNumber',
        'time_stamp': 'TimeStamp',
        'content': 'Content'
    }

    def __init__(self, frame_number=None, time_stamp=None, content=None):  # noqa: E501
        """StillFrame - a model defined in Swagger"""  # noqa: E501

        self._frame_number = None
        self._time_stamp = None
        self._content = None
        self.discriminator = None

        if frame_number is not None:
            self.frame_number = frame_number
        if time_stamp is not None:
            self.time_stamp = time_stamp
        if content is not None:
            self.content = content

    @property
    def frame_number(self):
        """Gets the frame_number of this StillFrame.  # noqa: E501

        The number of the current frame  # noqa: E501

        :return: The frame_number of this StillFrame.  # noqa: E501
        :rtype: int
        """
        return self._frame_number

    @frame_number.setter
    def frame_number(self, frame_number):
        """Sets the frame_number of this StillFrame.

        The number of the current frame  # noqa: E501

        :param frame_number: The frame_number of this StillFrame.  # noqa: E501
        :type: int
        """

        self._frame_number = frame_number

    @property
    def time_stamp(self):
        """Gets the time_stamp of this StillFrame.  # noqa: E501

        The playback time of the current frame  # noqa: E501

        :return: The time_stamp of this StillFrame.  # noqa: E501
        :rtype: str
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        """Sets the time_stamp of this StillFrame.

        The playback time of the current frame  # noqa: E501

        :param time_stamp: The time_stamp of this StillFrame.  # noqa: E501
        :type: str
        """

        self._time_stamp = time_stamp

    @property
    def content(self):
        """Gets the content of this StillFrame.  # noqa: E501

        The still frame in PNG format as a byte array  # noqa: E501

        :return: The content of this StillFrame.  # noqa: E501
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this StillFrame.

        The still frame in PNG format as a byte array  # noqa: E501

        :param content: The content of this StillFrame.  # noqa: E501
        :type: str
        """
        if content is not None and not re.search(r'^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', content):  # noqa: E501
            raise ValueError(r"Invalid value for `content`, must be a follow pattern or equal to `/^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$/`")  # noqa: E501

        self._content = content

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
        if issubclass(StillFrame, dict):
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
        if not isinstance(other, StillFrame):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
