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

class DatasetJob(object):
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
        'config': 'object',
        'execution_id': 'str',
        'status': 'str',
        'dataset_id': 'str',
        'dataset': 'Dataset',
        'dataset_job_statuses': 'list[DatasetJobStatus]',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'config': 'config',
        'execution_id': 'executionId',
        'status': 'status',
        'dataset_id': 'datasetId',
        'dataset': 'dataset',
        'dataset_job_statuses': 'datasetJobStatuses',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, config=None, execution_id=None, status=None, dataset_id=None, dataset=None, dataset_job_statuses=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """DatasetJob - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._config = None
        self._execution_id = None
        self._status = None
        self._dataset_id = None
        self._dataset = None
        self._dataset_job_statuses = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if config is not None:
            self.config = config
        if execution_id is not None:
            self.execution_id = execution_id
        if status is not None:
            self.status = status
        self.dataset_id = dataset_id
        if dataset is not None:
            self.dataset = dataset
        if dataset_job_statuses is not None:
            self.dataset_job_statuses = dataset_job_statuses
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
        """Gets the id of this DatasetJob.  # noqa: E501


        :return: The id of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DatasetJob.


        :param id: The id of this DatasetJob.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def config(self):
        """Gets the config of this DatasetJob.  # noqa: E501


        :return: The config of this DatasetJob.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this DatasetJob.


        :param config: The config of this DatasetJob.  # noqa: E501
        :type: object
        """

        self._config = config

    @property
    def execution_id(self):
        """Gets the execution_id of this DatasetJob.  # noqa: E501


        :return: The execution_id of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this DatasetJob.


        :param execution_id: The execution_id of this DatasetJob.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def status(self):
        """Gets the status of this DatasetJob.  # noqa: E501


        :return: The status of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DatasetJob.


        :param status: The status of this DatasetJob.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def dataset_id(self):
        """Gets the dataset_id of this DatasetJob.  # noqa: E501


        :return: The dataset_id of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this DatasetJob.


        :param dataset_id: The dataset_id of this DatasetJob.  # noqa: E501
        :type: str
        """
        if dataset_id is None:
            raise ValueError("Invalid value for `dataset_id`, must not be `None`")  # noqa: E501

        self._dataset_id = dataset_id

    @property
    def dataset(self):
        """Gets the dataset of this DatasetJob.  # noqa: E501


        :return: The dataset of this DatasetJob.  # noqa: E501
        :rtype: Dataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this DatasetJob.


        :param dataset: The dataset of this DatasetJob.  # noqa: E501
        :type: Dataset
        """

        self._dataset = dataset

    @property
    def dataset_job_statuses(self):
        """Gets the dataset_job_statuses of this DatasetJob.  # noqa: E501


        :return: The dataset_job_statuses of this DatasetJob.  # noqa: E501
        :rtype: list[DatasetJobStatus]
        """
        return self._dataset_job_statuses

    @dataset_job_statuses.setter
    def dataset_job_statuses(self, dataset_job_statuses):
        """Sets the dataset_job_statuses of this DatasetJob.


        :param dataset_job_statuses: The dataset_job_statuses of this DatasetJob.  # noqa: E501
        :type: list[DatasetJobStatus]
        """

        self._dataset_job_statuses = dataset_job_statuses

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this DatasetJob.  # noqa: E501


        :return: The last_updated_by of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this DatasetJob.


        :param last_updated_by: The last_updated_by of this DatasetJob.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this DatasetJob.  # noqa: E501


        :return: The created_by of this DatasetJob.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this DatasetJob.


        :param created_by: The created_by of this DatasetJob.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this DatasetJob.  # noqa: E501


        :return: The created_at of this DatasetJob.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DatasetJob.


        :param created_at: The created_at of this DatasetJob.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this DatasetJob.  # noqa: E501


        :return: The updated_at of this DatasetJob.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DatasetJob.


        :param updated_at: The updated_at of this DatasetJob.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this DatasetJob.  # noqa: E501


        :return: The version of this DatasetJob.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DatasetJob.


        :param version: The version of this DatasetJob.  # noqa: E501
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
        if issubclass(DatasetJob, dict):
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
        if not isinstance(other, DatasetJob):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
