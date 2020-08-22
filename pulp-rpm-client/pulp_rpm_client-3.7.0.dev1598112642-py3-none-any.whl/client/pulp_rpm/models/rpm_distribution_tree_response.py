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

from pulpcore.client.pulp_rpm.configuration import Configuration


class RpmDistributionTreeResponse(object):
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
        'pulp_href': 'str',
        'header_version': 'str',
        'release_name': 'str',
        'release_short': 'str',
        'release_version': 'str',
        'release_is_layered': 'bool',
        'base_product_name': 'str',
        'base_product_short': 'str',
        'base_product_version': 'str',
        'arch': 'str',
        'build_timestamp': 'float',
        'instimage': 'str',
        'mainimage': 'str',
        'discnum': 'int',
        'totaldiscs': 'int',
        'addons': 'list[AddonResponse]',
        'checksums': 'list[ChecksumResponse]',
        'images': 'list[ImageResponse]',
        'variants': 'list[VariantResponse]'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'header_version': 'header_version',
        'release_name': 'release_name',
        'release_short': 'release_short',
        'release_version': 'release_version',
        'release_is_layered': 'release_is_layered',
        'base_product_name': 'base_product_name',
        'base_product_short': 'base_product_short',
        'base_product_version': 'base_product_version',
        'arch': 'arch',
        'build_timestamp': 'build_timestamp',
        'instimage': 'instimage',
        'mainimage': 'mainimage',
        'discnum': 'discnum',
        'totaldiscs': 'totaldiscs',
        'addons': 'addons',
        'checksums': 'checksums',
        'images': 'images',
        'variants': 'variants'
    }

    def __init__(self, pulp_href=None, header_version=None, release_name=None, release_short=None, release_version=None, release_is_layered=None, base_product_name=None, base_product_short=None, base_product_version=None, arch=None, build_timestamp=None, instimage=None, mainimage=None, discnum=None, totaldiscs=None, addons=None, checksums=None, images=None, variants=None, local_vars_configuration=None):  # noqa: E501
        """RpmDistributionTreeResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._header_version = None
        self._release_name = None
        self._release_short = None
        self._release_version = None
        self._release_is_layered = None
        self._base_product_name = None
        self._base_product_short = None
        self._base_product_version = None
        self._arch = None
        self._build_timestamp = None
        self._instimage = None
        self._mainimage = None
        self._discnum = None
        self._totaldiscs = None
        self._addons = None
        self._checksums = None
        self._images = None
        self._variants = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        self.header_version = header_version
        self.release_name = release_name
        self.release_short = release_short
        self.release_version = release_version
        self.release_is_layered = release_is_layered
        self.base_product_name = base_product_name
        self.base_product_short = base_product_short
        self.base_product_version = base_product_version
        self.arch = arch
        self.build_timestamp = build_timestamp
        self.instimage = instimage
        self.mainimage = mainimage
        self.discnum = discnum
        self.totaldiscs = totaldiscs
        self.addons = addons
        self.checksums = checksums
        self.images = images
        self.variants = variants

    @property
    def pulp_href(self):
        """Gets the pulp_href of this RpmDistributionTreeResponse.  # noqa: E501


        :return: The pulp_href of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this RpmDistributionTreeResponse.


        :param pulp_href: The pulp_href of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def header_version(self):
        """Gets the header_version of this RpmDistributionTreeResponse.  # noqa: E501

        Header Version.  # noqa: E501

        :return: The header_version of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._header_version

    @header_version.setter
    def header_version(self, header_version):
        """Sets the header_version of this RpmDistributionTreeResponse.

        Header Version.  # noqa: E501

        :param header_version: The header_version of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and header_version is None:  # noqa: E501
            raise ValueError("Invalid value for `header_version`, must not be `None`")  # noqa: E501

        self._header_version = header_version

    @property
    def release_name(self):
        """Gets the release_name of this RpmDistributionTreeResponse.  # noqa: E501

        Release name.  # noqa: E501

        :return: The release_name of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._release_name

    @release_name.setter
    def release_name(self, release_name):
        """Sets the release_name of this RpmDistributionTreeResponse.

        Release name.  # noqa: E501

        :param release_name: The release_name of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and release_name is None:  # noqa: E501
            raise ValueError("Invalid value for `release_name`, must not be `None`")  # noqa: E501

        self._release_name = release_name

    @property
    def release_short(self):
        """Gets the release_short of this RpmDistributionTreeResponse.  # noqa: E501

        Release short name.  # noqa: E501

        :return: The release_short of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._release_short

    @release_short.setter
    def release_short(self, release_short):
        """Sets the release_short of this RpmDistributionTreeResponse.

        Release short name.  # noqa: E501

        :param release_short: The release_short of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and release_short is None:  # noqa: E501
            raise ValueError("Invalid value for `release_short`, must not be `None`")  # noqa: E501

        self._release_short = release_short

    @property
    def release_version(self):
        """Gets the release_version of this RpmDistributionTreeResponse.  # noqa: E501

        Release version.  # noqa: E501

        :return: The release_version of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._release_version

    @release_version.setter
    def release_version(self, release_version):
        """Sets the release_version of this RpmDistributionTreeResponse.

        Release version.  # noqa: E501

        :param release_version: The release_version of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and release_version is None:  # noqa: E501
            raise ValueError("Invalid value for `release_version`, must not be `None`")  # noqa: E501

        self._release_version = release_version

    @property
    def release_is_layered(self):
        """Gets the release_is_layered of this RpmDistributionTreeResponse.  # noqa: E501

        Typically False for an operating system, True otherwise.  # noqa: E501

        :return: The release_is_layered of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: bool
        """
        return self._release_is_layered

    @release_is_layered.setter
    def release_is_layered(self, release_is_layered):
        """Sets the release_is_layered of this RpmDistributionTreeResponse.

        Typically False for an operating system, True otherwise.  # noqa: E501

        :param release_is_layered: The release_is_layered of this RpmDistributionTreeResponse.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and release_is_layered is None:  # noqa: E501
            raise ValueError("Invalid value for `release_is_layered`, must not be `None`")  # noqa: E501

        self._release_is_layered = release_is_layered

    @property
    def base_product_name(self):
        """Gets the base_product_name of this RpmDistributionTreeResponse.  # noqa: E501

        Base Product name.  # noqa: E501

        :return: The base_product_name of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._base_product_name

    @base_product_name.setter
    def base_product_name(self, base_product_name):
        """Sets the base_product_name of this RpmDistributionTreeResponse.

        Base Product name.  # noqa: E501

        :param base_product_name: The base_product_name of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._base_product_name = base_product_name

    @property
    def base_product_short(self):
        """Gets the base_product_short of this RpmDistributionTreeResponse.  # noqa: E501

        Base Product short name.  # noqa: E501

        :return: The base_product_short of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._base_product_short

    @base_product_short.setter
    def base_product_short(self, base_product_short):
        """Sets the base_product_short of this RpmDistributionTreeResponse.

        Base Product short name.  # noqa: E501

        :param base_product_short: The base_product_short of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._base_product_short = base_product_short

    @property
    def base_product_version(self):
        """Gets the base_product_version of this RpmDistributionTreeResponse.  # noqa: E501

        Base Product version.  # noqa: E501

        :return: The base_product_version of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._base_product_version

    @base_product_version.setter
    def base_product_version(self, base_product_version):
        """Sets the base_product_version of this RpmDistributionTreeResponse.

        Base Product version.  # noqa: E501

        :param base_product_version: The base_product_version of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._base_product_version = base_product_version

    @property
    def arch(self):
        """Gets the arch of this RpmDistributionTreeResponse.  # noqa: E501

        Tree architecturerch.  # noqa: E501

        :return: The arch of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._arch

    @arch.setter
    def arch(self, arch):
        """Sets the arch of this RpmDistributionTreeResponse.

        Tree architecturerch.  # noqa: E501

        :param arch: The arch of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and arch is None:  # noqa: E501
            raise ValueError("Invalid value for `arch`, must not be `None`")  # noqa: E501

        self._arch = arch

    @property
    def build_timestamp(self):
        """Gets the build_timestamp of this RpmDistributionTreeResponse.  # noqa: E501

        Tree build time timestamp.  # noqa: E501

        :return: The build_timestamp of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: float
        """
        return self._build_timestamp

    @build_timestamp.setter
    def build_timestamp(self, build_timestamp):
        """Sets the build_timestamp of this RpmDistributionTreeResponse.

        Tree build time timestamp.  # noqa: E501

        :param build_timestamp: The build_timestamp of this RpmDistributionTreeResponse.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and build_timestamp is None:  # noqa: E501
            raise ValueError("Invalid value for `build_timestamp`, must not be `None`")  # noqa: E501

        self._build_timestamp = build_timestamp

    @property
    def instimage(self):
        """Gets the instimage of this RpmDistributionTreeResponse.  # noqa: E501

        Relative path to Anaconda instimage.  # noqa: E501

        :return: The instimage of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._instimage

    @instimage.setter
    def instimage(self, instimage):
        """Sets the instimage of this RpmDistributionTreeResponse.

        Relative path to Anaconda instimage.  # noqa: E501

        :param instimage: The instimage of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._instimage = instimage

    @property
    def mainimage(self):
        """Gets the mainimage of this RpmDistributionTreeResponse.  # noqa: E501

        Relative path to Anaconda stage2 image.  # noqa: E501

        :return: The mainimage of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: str
        """
        return self._mainimage

    @mainimage.setter
    def mainimage(self, mainimage):
        """Sets the mainimage of this RpmDistributionTreeResponse.

        Relative path to Anaconda stage2 image.  # noqa: E501

        :param mainimage: The mainimage of this RpmDistributionTreeResponse.  # noqa: E501
        :type: str
        """

        self._mainimage = mainimage

    @property
    def discnum(self):
        """Gets the discnum of this RpmDistributionTreeResponse.  # noqa: E501

        Disc number.  # noqa: E501

        :return: The discnum of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: int
        """
        return self._discnum

    @discnum.setter
    def discnum(self, discnum):
        """Sets the discnum of this RpmDistributionTreeResponse.

        Disc number.  # noqa: E501

        :param discnum: The discnum of this RpmDistributionTreeResponse.  # noqa: E501
        :type: int
        """

        self._discnum = discnum

    @property
    def totaldiscs(self):
        """Gets the totaldiscs of this RpmDistributionTreeResponse.  # noqa: E501

        Number of discs in media set.  # noqa: E501

        :return: The totaldiscs of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: int
        """
        return self._totaldiscs

    @totaldiscs.setter
    def totaldiscs(self, totaldiscs):
        """Sets the totaldiscs of this RpmDistributionTreeResponse.

        Number of discs in media set.  # noqa: E501

        :param totaldiscs: The totaldiscs of this RpmDistributionTreeResponse.  # noqa: E501
        :type: int
        """

        self._totaldiscs = totaldiscs

    @property
    def addons(self):
        """Gets the addons of this RpmDistributionTreeResponse.  # noqa: E501


        :return: The addons of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: list[AddonResponse]
        """
        return self._addons

    @addons.setter
    def addons(self, addons):
        """Sets the addons of this RpmDistributionTreeResponse.


        :param addons: The addons of this RpmDistributionTreeResponse.  # noqa: E501
        :type: list[AddonResponse]
        """
        if self.local_vars_configuration.client_side_validation and addons is None:  # noqa: E501
            raise ValueError("Invalid value for `addons`, must not be `None`")  # noqa: E501

        self._addons = addons

    @property
    def checksums(self):
        """Gets the checksums of this RpmDistributionTreeResponse.  # noqa: E501


        :return: The checksums of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: list[ChecksumResponse]
        """
        return self._checksums

    @checksums.setter
    def checksums(self, checksums):
        """Sets the checksums of this RpmDistributionTreeResponse.


        :param checksums: The checksums of this RpmDistributionTreeResponse.  # noqa: E501
        :type: list[ChecksumResponse]
        """
        if self.local_vars_configuration.client_side_validation and checksums is None:  # noqa: E501
            raise ValueError("Invalid value for `checksums`, must not be `None`")  # noqa: E501

        self._checksums = checksums

    @property
    def images(self):
        """Gets the images of this RpmDistributionTreeResponse.  # noqa: E501


        :return: The images of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: list[ImageResponse]
        """
        return self._images

    @images.setter
    def images(self, images):
        """Sets the images of this RpmDistributionTreeResponse.


        :param images: The images of this RpmDistributionTreeResponse.  # noqa: E501
        :type: list[ImageResponse]
        """
        if self.local_vars_configuration.client_side_validation and images is None:  # noqa: E501
            raise ValueError("Invalid value for `images`, must not be `None`")  # noqa: E501

        self._images = images

    @property
    def variants(self):
        """Gets the variants of this RpmDistributionTreeResponse.  # noqa: E501


        :return: The variants of this RpmDistributionTreeResponse.  # noqa: E501
        :rtype: list[VariantResponse]
        """
        return self._variants

    @variants.setter
    def variants(self, variants):
        """Sets the variants of this RpmDistributionTreeResponse.


        :param variants: The variants of this RpmDistributionTreeResponse.  # noqa: E501
        :type: list[VariantResponse]
        """
        if self.local_vars_configuration.client_side_validation and variants is None:  # noqa: E501
            raise ValueError("Invalid value for `variants`, must not be `None`")  # noqa: E501

        self._variants = variants

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
        if not isinstance(other, RpmDistributionTreeResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RpmDistributionTreeResponse):
            return True

        return self.to_dict() != other.to_dict()
