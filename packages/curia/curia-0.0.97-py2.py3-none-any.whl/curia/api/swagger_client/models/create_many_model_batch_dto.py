# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 1.25.0-develop.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateManyModelBatchDto(object):
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
        'bulk': 'list[ModelBatch]'
    }

    attribute_map = {
        'bulk': 'bulk'
    }

    def __init__(self, bulk=None):  # noqa: E501
        """CreateManyModelBatchDto - a model defined in Swagger"""  # noqa: E501
        self._bulk = None
        self.discriminator = None
        self.bulk = bulk

    @property
    def bulk(self):
        """Gets the bulk of this CreateManyModelBatchDto.  # noqa: E501


        :return: The bulk of this CreateManyModelBatchDto.  # noqa: E501
        :rtype: list[ModelBatch]
        """
        return self._bulk

    @bulk.setter
    def bulk(self, bulk):
        """Sets the bulk of this CreateManyModelBatchDto.


        :param bulk: The bulk of this CreateManyModelBatchDto.  # noqa: E501
        :type: list[ModelBatch]
        """
        if bulk is None:
            raise ValueError("Invalid value for `bulk`, must not be `None`")  # noqa: E501

        self._bulk = bulk

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
        if issubclass(CreateManyModelBatchDto, dict):
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
        if not isinstance(other, CreateManyModelBatchDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
