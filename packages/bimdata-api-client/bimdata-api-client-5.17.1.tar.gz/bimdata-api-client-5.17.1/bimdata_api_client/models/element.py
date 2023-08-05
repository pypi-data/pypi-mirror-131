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


class Element(object):
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
        'uuid': 'str',
        'type': 'str',
        'attributes': 'PropertySet',
        'property_sets': 'list[PropertySet]',
        'classifications': 'list[Classification]',
        'material_list': 'list[MaterialListComponent]',
        'layers': 'list[LayerElement]'
    }

    attribute_map = {
        'id': 'id',
        'uuid': 'uuid',
        'type': 'type',
        'attributes': 'attributes',
        'property_sets': 'property_sets',
        'classifications': 'classifications',
        'material_list': 'material_list',
        'layers': 'layers'
    }

    def __init__(self, id=None, uuid=None, type=None, attributes=None, property_sets=None, classifications=None, material_list=None, layers=None, local_vars_configuration=None):  # noqa: E501
        """Element - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._uuid = None
        self._type = None
        self._attributes = None
        self._property_sets = None
        self._classifications = None
        self._material_list = None
        self._layers = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if uuid is not None:
            self.uuid = uuid
        self.type = type
        if attributes is not None:
            self.attributes = attributes
        if property_sets is not None:
            self.property_sets = property_sets
        if classifications is not None:
            self.classifications = classifications
        if material_list is not None:
            self.material_list = material_list
        if layers is not None:
            self.layers = layers

    @property
    def id(self):
        """Gets the id of this Element.  # noqa: E501


        :return: The id of this Element.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Element.


        :param id: The id of this Element.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def uuid(self):
        """Gets the uuid of this Element.  # noqa: E501


        :return: The uuid of this Element.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this Element.


        :param uuid: The uuid of this Element.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                uuid is not None and len(uuid) > 22):
            raise ValueError("Invalid value for `uuid`, length must be less than or equal to `22`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                uuid is not None and len(uuid) < 22):
            raise ValueError("Invalid value for `uuid`, length must be greater than or equal to `22`")  # noqa: E501

        self._uuid = uuid

    @property
    def type(self):
        """Gets the type of this Element.  # noqa: E501

        IFC type for the element  # noqa: E501

        :return: The type of this Element.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Element.

        IFC type for the element  # noqa: E501

        :param type: The type of this Element.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) > 64):
            raise ValueError("Invalid value for `type`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def attributes(self):
        """Gets the attributes of this Element.  # noqa: E501


        :return: The attributes of this Element.  # noqa: E501
        :rtype: PropertySet
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this Element.


        :param attributes: The attributes of this Element.  # noqa: E501
        :type: PropertySet
        """

        self._attributes = attributes

    @property
    def property_sets(self):
        """Gets the property_sets of this Element.  # noqa: E501


        :return: The property_sets of this Element.  # noqa: E501
        :rtype: list[PropertySet]
        """
        return self._property_sets

    @property_sets.setter
    def property_sets(self, property_sets):
        """Sets the property_sets of this Element.


        :param property_sets: The property_sets of this Element.  # noqa: E501
        :type: list[PropertySet]
        """

        self._property_sets = property_sets

    @property
    def classifications(self):
        """Gets the classifications of this Element.  # noqa: E501


        :return: The classifications of this Element.  # noqa: E501
        :rtype: list[Classification]
        """
        return self._classifications

    @classifications.setter
    def classifications(self, classifications):
        """Sets the classifications of this Element.


        :param classifications: The classifications of this Element.  # noqa: E501
        :type: list[Classification]
        """

        self._classifications = classifications

    @property
    def material_list(self):
        """Gets the material_list of this Element.  # noqa: E501


        :return: The material_list of this Element.  # noqa: E501
        :rtype: list[MaterialListComponent]
        """
        return self._material_list

    @material_list.setter
    def material_list(self, material_list):
        """Sets the material_list of this Element.


        :param material_list: The material_list of this Element.  # noqa: E501
        :type: list[MaterialListComponent]
        """

        self._material_list = material_list

    @property
    def layers(self):
        """Gets the layers of this Element.  # noqa: E501


        :return: The layers of this Element.  # noqa: E501
        :rtype: list[LayerElement]
        """
        return self._layers

    @layers.setter
    def layers(self, layers):
        """Sets the layers of this Element.


        :param layers: The layers of this Element.  # noqa: E501
        :type: list[LayerElement]
        """

        self._layers = layers

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
        if not isinstance(other, Element):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Element):
            return True

        return self.to_dict() != other.to_dict()
