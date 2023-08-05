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


class Space(object):
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
        'id': 'int',
        'name': 'str',
        'longname': 'str',
        'uuid': 'str',
        'zone_set': 'list[int]',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'longname': 'longname',
        'uuid': 'uuid',
        'zone_set': 'zone_set',
        'created_at': 'created_at',
        'updated_at': 'updated_at'
    }

    def __init__(self, id=None, name=None, longname=None, uuid=None, zone_set=None, created_at=None, updated_at=None, local_vars_configuration=None):  # noqa: E501
        """Space - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._longname = None
        self._uuid = None
        self._zone_set = None
        self._created_at = None
        self._updated_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.longname = longname
        self.uuid = uuid
        if zone_set is not None:
            self.zone_set = zone_set
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def id(self):
        """Gets the id of this Space.  # noqa: E501


        :return: The id of this Space.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Space.


        :param id: The id of this Space.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Space.  # noqa: E501


        :return: The name of this Space.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Space.


        :param name: The name of this Space.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 255):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `255`")  # noqa: E501

        self._name = name

    @property
    def longname(self):
        """Gets the longname of this Space.  # noqa: E501


        :return: The longname of this Space.  # noqa: E501
        :rtype: str
        """
        return self._longname

    @longname.setter
    def longname(self, longname):
        """Sets the longname of this Space.


        :param longname: The longname of this Space.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                longname is not None and len(longname) > 255):
            raise ValueError("Invalid value for `longname`, length must be less than or equal to `255`")  # noqa: E501

        self._longname = longname

    @property
    def uuid(self):
        """Gets the uuid of this Space.  # noqa: E501


        :return: The uuid of this Space.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this Space.


        :param uuid: The uuid of this Space.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and uuid is None:  # noqa: E501
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                uuid is not None and len(uuid) > 512):
            raise ValueError("Invalid value for `uuid`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                uuid is not None and len(uuid) < 1):
            raise ValueError("Invalid value for `uuid`, length must be greater than or equal to `1`")  # noqa: E501

        self._uuid = uuid

    @property
    def zone_set(self):
        """Gets the zone_set of this Space.  # noqa: E501


        :return: The zone_set of this Space.  # noqa: E501
        :rtype: list[int]
        """
        return self._zone_set

    @zone_set.setter
    def zone_set(self, zone_set):
        """Sets the zone_set of this Space.


        :param zone_set: The zone_set of this Space.  # noqa: E501
        :type: list[int]
        """

        self._zone_set = zone_set

    @property
    def created_at(self):
        """Gets the created_at of this Space.  # noqa: E501


        :return: The created_at of this Space.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Space.


        :param created_at: The created_at of this Space.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Space.  # noqa: E501


        :return: The updated_at of this Space.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Space.


        :param updated_at: The updated_at of this Space.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

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
        if not isinstance(other, Space):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Space):
            return True

        return self.to_dict() != other.to_dict()
