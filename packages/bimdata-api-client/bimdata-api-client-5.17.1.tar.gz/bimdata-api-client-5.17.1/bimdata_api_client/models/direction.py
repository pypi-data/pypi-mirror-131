# coding: utf-8

"""
    BIMData API

    BIMData API is a tool to interact with your models stored on BIMData’s servers.     Through the API, you can manage your projects, the clouds, upload your IFC files and manage them through endpoints.  # noqa: E501

    The version of the OpenAPI document: v1
    Contact: support@bimdata.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from bimdata_api_client.configuration import Configuration


class Direction(object):
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
        'x': 'float',
        'y': 'float',
        'z': 'float'
    }

    attribute_map = {
        'x': 'x',
        'y': 'y',
        'z': 'z'
    }

    def __init__(self, x=None, y=None, z=None, local_vars_configuration=None):  # noqa: E501
        """Direction - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._x = None
        self._y = None
        self._z = None
        self.discriminator = None

        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self):
        """Gets the x of this Direction.  # noqa: E501


        :return: The x of this Direction.  # noqa: E501
        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, x):
        """Sets the x of this Direction.


        :param x: The x of this Direction.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and x is None:  # noqa: E501
            raise ValueError("Invalid value for `x`, must not be `None`")  # noqa: E501

        self._x = x

    @property
    def y(self):
        """Gets the y of this Direction.  # noqa: E501


        :return: The y of this Direction.  # noqa: E501
        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, y):
        """Sets the y of this Direction.


        :param y: The y of this Direction.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and y is None:  # noqa: E501
            raise ValueError("Invalid value for `y`, must not be `None`")  # noqa: E501

        self._y = y

    @property
    def z(self):
        """Gets the z of this Direction.  # noqa: E501


        :return: The z of this Direction.  # noqa: E501
        :rtype: float
        """
        return self._z

    @z.setter
    def z(self, z):
        """Sets the z of this Direction.


        :param z: The z of this Direction.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and z is None:  # noqa: E501
            raise ValueError("Invalid value for `z`, must not be `None`")  # noqa: E501

        self._z = z

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
        if not isinstance(other, Direction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Direction):
            return True

        return self.to_dict() != other.to_dict()
