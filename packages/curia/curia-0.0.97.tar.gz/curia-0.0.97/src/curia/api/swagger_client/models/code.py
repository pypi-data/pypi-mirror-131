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

class Code(object):
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
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'description': 'str',
        'code_range': 'str',
        'match_column_name': 'str',
        'match_column_value': 'str',
        'hierarchy_level': 'float',
        'parent_code_id': 'str',
        'parent_code': 'Code',
        'children_codes': 'list[Code]',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'description': 'description',
        'code_range': 'codeRange',
        'match_column_name': 'matchColumnName',
        'match_column_value': 'matchColumnValue',
        'hierarchy_level': 'hierarchyLevel',
        'parent_code_id': 'parentCodeId',
        'parent_code': 'parentCode',
        'children_codes': 'childrenCodes',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, type=None, description=None, code_range=None, match_column_name=None, match_column_value=None, hierarchy_level=None, parent_code_id=None, parent_code=None, children_codes=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Code - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._type = None
        self._description = None
        self._code_range = None
        self._match_column_name = None
        self._match_column_value = None
        self._hierarchy_level = None
        self._parent_code_id = None
        self._parent_code = None
        self._children_codes = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        self.type = type
        if description is not None:
            self.description = description
        self.code_range = code_range
        self.match_column_name = match_column_name
        self.match_column_value = match_column_value
        self.hierarchy_level = hierarchy_level
        if parent_code_id is not None:
            self.parent_code_id = parent_code_id
        if parent_code is not None:
            self.parent_code = parent_code
        if children_codes is not None:
            self.children_codes = children_codes
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this Code.  # noqa: E501


        :return: The id of this Code.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Code.


        :param id: The id of this Code.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Code.  # noqa: E501


        :return: The name of this Code.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Code.


        :param name: The name of this Code.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this Code.  # noqa: E501


        :return: The type of this Code.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Code.


        :param type: The type of this Code.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["diagnosis", "procedure", "custom", "prescription", "dme"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def description(self):
        """Gets the description of this Code.  # noqa: E501


        :return: The description of this Code.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Code.


        :param description: The description of this Code.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def code_range(self):
        """Gets the code_range of this Code.  # noqa: E501


        :return: The code_range of this Code.  # noqa: E501
        :rtype: str
        """
        return self._code_range

    @code_range.setter
    def code_range(self, code_range):
        """Sets the code_range of this Code.


        :param code_range: The code_range of this Code.  # noqa: E501
        :type: str
        """
        if code_range is None:
            raise ValueError("Invalid value for `code_range`, must not be `None`")  # noqa: E501

        self._code_range = code_range

    @property
    def match_column_name(self):
        """Gets the match_column_name of this Code.  # noqa: E501


        :return: The match_column_name of this Code.  # noqa: E501
        :rtype: str
        """
        return self._match_column_name

    @match_column_name.setter
    def match_column_name(self, match_column_name):
        """Sets the match_column_name of this Code.


        :param match_column_name: The match_column_name of this Code.  # noqa: E501
        :type: str
        """
        if match_column_name is None:
            raise ValueError("Invalid value for `match_column_name`, must not be `None`")  # noqa: E501

        self._match_column_name = match_column_name

    @property
    def match_column_value(self):
        """Gets the match_column_value of this Code.  # noqa: E501


        :return: The match_column_value of this Code.  # noqa: E501
        :rtype: str
        """
        return self._match_column_value

    @match_column_value.setter
    def match_column_value(self, match_column_value):
        """Sets the match_column_value of this Code.


        :param match_column_value: The match_column_value of this Code.  # noqa: E501
        :type: str
        """
        if match_column_value is None:
            raise ValueError("Invalid value for `match_column_value`, must not be `None`")  # noqa: E501

        self._match_column_value = match_column_value

    @property
    def hierarchy_level(self):
        """Gets the hierarchy_level of this Code.  # noqa: E501


        :return: The hierarchy_level of this Code.  # noqa: E501
        :rtype: float
        """
        return self._hierarchy_level

    @hierarchy_level.setter
    def hierarchy_level(self, hierarchy_level):
        """Sets the hierarchy_level of this Code.


        :param hierarchy_level: The hierarchy_level of this Code.  # noqa: E501
        :type: float
        """
        if hierarchy_level is None:
            raise ValueError("Invalid value for `hierarchy_level`, must not be `None`")  # noqa: E501

        self._hierarchy_level = hierarchy_level

    @property
    def parent_code_id(self):
        """Gets the parent_code_id of this Code.  # noqa: E501


        :return: The parent_code_id of this Code.  # noqa: E501
        :rtype: str
        """
        return self._parent_code_id

    @parent_code_id.setter
    def parent_code_id(self, parent_code_id):
        """Sets the parent_code_id of this Code.


        :param parent_code_id: The parent_code_id of this Code.  # noqa: E501
        :type: str
        """

        self._parent_code_id = parent_code_id

    @property
    def parent_code(self):
        """Gets the parent_code of this Code.  # noqa: E501


        :return: The parent_code of this Code.  # noqa: E501
        :rtype: Code
        """
        return self._parent_code

    @parent_code.setter
    def parent_code(self, parent_code):
        """Sets the parent_code of this Code.


        :param parent_code: The parent_code of this Code.  # noqa: E501
        :type: Code
        """

        self._parent_code = parent_code

    @property
    def children_codes(self):
        """Gets the children_codes of this Code.  # noqa: E501


        :return: The children_codes of this Code.  # noqa: E501
        :rtype: list[Code]
        """
        return self._children_codes

    @children_codes.setter
    def children_codes(self, children_codes):
        """Sets the children_codes of this Code.


        :param children_codes: The children_codes of this Code.  # noqa: E501
        :type: list[Code]
        """

        self._children_codes = children_codes

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this Code.  # noqa: E501


        :return: The last_updated_by of this Code.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this Code.


        :param last_updated_by: The last_updated_by of this Code.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this Code.  # noqa: E501


        :return: The created_by of this Code.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Code.


        :param created_by: The created_by of this Code.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this Code.  # noqa: E501


        :return: The created_at of this Code.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Code.


        :param created_at: The created_at of this Code.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Code.  # noqa: E501


        :return: The updated_at of this Code.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Code.


        :param updated_at: The updated_at of this Code.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Code.  # noqa: E501


        :return: The version of this Code.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Code.


        :param version: The version of this Code.  # noqa: E501
        :type: float
        """

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
        if issubclass(Code, dict):
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
        if not isinstance(other, Code):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
