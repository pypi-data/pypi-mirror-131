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

class ModelPopulation(object):
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
        'organization_id': 'str',
        'organization': 'Organization',
        'cohorts': 'list[CohortDefinition]',
        'outcome': 'OutcomeDefinition',
        'intervention': 'InterventionDefinition',
        'features': 'list[Feature]',
        'cohort_results': 'list[CohortResults]',
        'data_query_id': 'str',
        'data_query': 'DataQuery',
        'model_job': 'ModelJob',
        'created_at': 'datetime',
        'created_by': 'str',
        'updated_at': 'datetime',
        'last_updated_by': 'str',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'organization_id': 'organizationId',
        'organization': 'organization',
        'cohorts': 'cohorts',
        'outcome': 'outcome',
        'intervention': 'intervention',
        'features': 'features',
        'cohort_results': 'cohortResults',
        'data_query_id': 'dataQueryId',
        'data_query': 'dataQuery',
        'model_job': 'modelJob',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'updated_at': 'updatedAt',
        'last_updated_by': 'lastUpdatedBy',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, organization_id=None, organization=None, cohorts=None, outcome=None, intervention=None, features=None, cohort_results=None, data_query_id=None, data_query=None, model_job=None, created_at=None, created_by=None, updated_at=None, last_updated_by=None, version=None):  # noqa: E501
        """ModelPopulation - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._organization_id = None
        self._organization = None
        self._cohorts = None
        self._outcome = None
        self._intervention = None
        self._features = None
        self._cohort_results = None
        self._data_query_id = None
        self._data_query = None
        self._model_job = None
        self._created_at = None
        self._created_by = None
        self._updated_at = None
        self._last_updated_by = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if organization_id is not None:
            self.organization_id = organization_id
        if organization is not None:
            self.organization = organization
        if cohorts is not None:
            self.cohorts = cohorts
        if outcome is not None:
            self.outcome = outcome
        if intervention is not None:
            self.intervention = intervention
        if features is not None:
            self.features = features
        if cohort_results is not None:
            self.cohort_results = cohort_results
        if data_query_id is not None:
            self.data_query_id = data_query_id
        if data_query is not None:
            self.data_query = data_query
        if model_job is not None:
            self.model_job = model_job
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if updated_at is not None:
            self.updated_at = updated_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this ModelPopulation.  # noqa: E501


        :return: The id of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelPopulation.


        :param id: The id of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ModelPopulation.  # noqa: E501


        :return: The name of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelPopulation.


        :param name: The name of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def organization_id(self):
        """Gets the organization_id of this ModelPopulation.  # noqa: E501


        :return: The organization_id of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this ModelPopulation.


        :param organization_id: The organization_id of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._organization_id = organization_id

    @property
    def organization(self):
        """Gets the organization of this ModelPopulation.  # noqa: E501


        :return: The organization of this ModelPopulation.  # noqa: E501
        :rtype: Organization
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """Sets the organization of this ModelPopulation.


        :param organization: The organization of this ModelPopulation.  # noqa: E501
        :type: Organization
        """

        self._organization = organization

    @property
    def cohorts(self):
        """Gets the cohorts of this ModelPopulation.  # noqa: E501


        :return: The cohorts of this ModelPopulation.  # noqa: E501
        :rtype: list[CohortDefinition]
        """
        return self._cohorts

    @cohorts.setter
    def cohorts(self, cohorts):
        """Sets the cohorts of this ModelPopulation.


        :param cohorts: The cohorts of this ModelPopulation.  # noqa: E501
        :type: list[CohortDefinition]
        """

        self._cohorts = cohorts

    @property
    def outcome(self):
        """Gets the outcome of this ModelPopulation.  # noqa: E501


        :return: The outcome of this ModelPopulation.  # noqa: E501
        :rtype: OutcomeDefinition
        """
        return self._outcome

    @outcome.setter
    def outcome(self, outcome):
        """Sets the outcome of this ModelPopulation.


        :param outcome: The outcome of this ModelPopulation.  # noqa: E501
        :type: OutcomeDefinition
        """

        self._outcome = outcome

    @property
    def intervention(self):
        """Gets the intervention of this ModelPopulation.  # noqa: E501


        :return: The intervention of this ModelPopulation.  # noqa: E501
        :rtype: InterventionDefinition
        """
        return self._intervention

    @intervention.setter
    def intervention(self, intervention):
        """Sets the intervention of this ModelPopulation.


        :param intervention: The intervention of this ModelPopulation.  # noqa: E501
        :type: InterventionDefinition
        """

        self._intervention = intervention

    @property
    def features(self):
        """Gets the features of this ModelPopulation.  # noqa: E501


        :return: The features of this ModelPopulation.  # noqa: E501
        :rtype: list[Feature]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this ModelPopulation.


        :param features: The features of this ModelPopulation.  # noqa: E501
        :type: list[Feature]
        """

        self._features = features

    @property
    def cohort_results(self):
        """Gets the cohort_results of this ModelPopulation.  # noqa: E501


        :return: The cohort_results of this ModelPopulation.  # noqa: E501
        :rtype: list[CohortResults]
        """
        return self._cohort_results

    @cohort_results.setter
    def cohort_results(self, cohort_results):
        """Sets the cohort_results of this ModelPopulation.


        :param cohort_results: The cohort_results of this ModelPopulation.  # noqa: E501
        :type: list[CohortResults]
        """

        self._cohort_results = cohort_results

    @property
    def data_query_id(self):
        """Gets the data_query_id of this ModelPopulation.  # noqa: E501


        :return: The data_query_id of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._data_query_id

    @data_query_id.setter
    def data_query_id(self, data_query_id):
        """Sets the data_query_id of this ModelPopulation.


        :param data_query_id: The data_query_id of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._data_query_id = data_query_id

    @property
    def data_query(self):
        """Gets the data_query of this ModelPopulation.  # noqa: E501


        :return: The data_query of this ModelPopulation.  # noqa: E501
        :rtype: DataQuery
        """
        return self._data_query

    @data_query.setter
    def data_query(self, data_query):
        """Sets the data_query of this ModelPopulation.


        :param data_query: The data_query of this ModelPopulation.  # noqa: E501
        :type: DataQuery
        """

        self._data_query = data_query

    @property
    def model_job(self):
        """Gets the model_job of this ModelPopulation.  # noqa: E501


        :return: The model_job of this ModelPopulation.  # noqa: E501
        :rtype: ModelJob
        """
        return self._model_job

    @model_job.setter
    def model_job(self, model_job):
        """Sets the model_job of this ModelPopulation.


        :param model_job: The model_job of this ModelPopulation.  # noqa: E501
        :type: ModelJob
        """

        self._model_job = model_job

    @property
    def created_at(self):
        """Gets the created_at of this ModelPopulation.  # noqa: E501


        :return: The created_at of this ModelPopulation.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelPopulation.


        :param created_at: The created_at of this ModelPopulation.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this ModelPopulation.  # noqa: E501


        :return: The created_by of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelPopulation.


        :param created_by: The created_by of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelPopulation.  # noqa: E501


        :return: The updated_at of this ModelPopulation.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelPopulation.


        :param updated_at: The updated_at of this ModelPopulation.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelPopulation.  # noqa: E501


        :return: The last_updated_by of this ModelPopulation.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelPopulation.


        :param last_updated_by: The last_updated_by of this ModelPopulation.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def version(self):
        """Gets the version of this ModelPopulation.  # noqa: E501


        :return: The version of this ModelPopulation.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelPopulation.


        :param version: The version of this ModelPopulation.  # noqa: E501
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
        if issubclass(ModelPopulation, dict):
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
        if not isinstance(other, ModelPopulation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
