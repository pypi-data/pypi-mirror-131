# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class OsImage(object):
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
        'openshift_version': 'str',
        'cpu_architecture': 'str',
        'url': 'str',
        'rootfs_url': 'str',
        'version': 'str'
    }

    attribute_map = {
        'openshift_version': 'openshift_version',
        'cpu_architecture': 'cpu_architecture',
        'url': 'url',
        'rootfs_url': 'rootfs_url',
        'version': 'version'
    }

    def __init__(self, openshift_version=None, cpu_architecture='x86_64', url=None, rootfs_url=None, version=None):  # noqa: E501
        """OsImage - a model defined in Swagger"""  # noqa: E501

        self._openshift_version = None
        self._cpu_architecture = None
        self._url = None
        self._rootfs_url = None
        self._version = None
        self.discriminator = None

        self.openshift_version = openshift_version
        self.cpu_architecture = cpu_architecture
        self.url = url
        self.rootfs_url = rootfs_url
        self.version = version

    @property
    def openshift_version(self):
        """Gets the openshift_version of this OsImage.  # noqa: E501

        Version of the OpenShift cluster.  # noqa: E501

        :return: The openshift_version of this OsImage.  # noqa: E501
        :rtype: str
        """
        return self._openshift_version

    @openshift_version.setter
    def openshift_version(self, openshift_version):
        """Sets the openshift_version of this OsImage.

        Version of the OpenShift cluster.  # noqa: E501

        :param openshift_version: The openshift_version of this OsImage.  # noqa: E501
        :type: str
        """
        if openshift_version is None:
            raise ValueError("Invalid value for `openshift_version`, must not be `None`")  # noqa: E501

        self._openshift_version = openshift_version

    @property
    def cpu_architecture(self):
        """Gets the cpu_architecture of this OsImage.  # noqa: E501

        The CPU architecture of the image (x86_64/arm64/etc).  # noqa: E501

        :return: The cpu_architecture of this OsImage.  # noqa: E501
        :rtype: str
        """
        return self._cpu_architecture

    @cpu_architecture.setter
    def cpu_architecture(self, cpu_architecture):
        """Sets the cpu_architecture of this OsImage.

        The CPU architecture of the image (x86_64/arm64/etc).  # noqa: E501

        :param cpu_architecture: The cpu_architecture of this OsImage.  # noqa: E501
        :type: str
        """
        if cpu_architecture is None:
            raise ValueError("Invalid value for `cpu_architecture`, must not be `None`")  # noqa: E501

        self._cpu_architecture = cpu_architecture

    @property
    def url(self):
        """Gets the url of this OsImage.  # noqa: E501

        The base OS image used for the discovery iso.  # noqa: E501

        :return: The url of this OsImage.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this OsImage.

        The base OS image used for the discovery iso.  # noqa: E501

        :param url: The url of this OsImage.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def rootfs_url(self):
        """Gets the rootfs_url of this OsImage.  # noqa: E501

        The OS rootfs url.  # noqa: E501

        :return: The rootfs_url of this OsImage.  # noqa: E501
        :rtype: str
        """
        return self._rootfs_url

    @rootfs_url.setter
    def rootfs_url(self, rootfs_url):
        """Sets the rootfs_url of this OsImage.

        The OS rootfs url.  # noqa: E501

        :param rootfs_url: The rootfs_url of this OsImage.  # noqa: E501
        :type: str
        """
        if rootfs_url is None:
            raise ValueError("Invalid value for `rootfs_url`, must not be `None`")  # noqa: E501

        self._rootfs_url = rootfs_url

    @property
    def version(self):
        """Gets the version of this OsImage.  # noqa: E501

        Build ID of the OS image.  # noqa: E501

        :return: The version of this OsImage.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this OsImage.

        Build ID of the OS image.  # noqa: E501

        :param version: The version of this OsImage.  # noqa: E501
        :type: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

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
        if issubclass(OsImage, dict):
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
        if not isinstance(other, OsImage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
