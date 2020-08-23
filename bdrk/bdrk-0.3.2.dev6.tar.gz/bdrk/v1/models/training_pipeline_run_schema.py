# coding: utf-8

"""
    Bedrock

    API documentation for Bedrock platform  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class TrainingPipelineRunSchema(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict):       The key is attribute name
                                  and the value is attribute type.
      attribute_map (dict):       The key is attribute name
                                  and the value is json key in definition.
      readonly_attributes (dict): Set of readonly attributes (will not be
                                  serialised in request body).
    """
    openapi_types = {
        'config_file_path': 'str',
        'created_at': 'datetime',
        'created_by': 'UserSchema',
        'entity_id': 'str',
        'entity_number': 'int',
        'environment_id': 'str',
        'id': 'str',
        'metrics': 'object',
        'model_artefact_id': 'str',
        'object': 'str',
        'pipeline_id': 'str',
        'schedule_number': 'int',
        'script_parameters': 'object',
        'secrets': 'object',
        'source': 'object',
        'status': 'str',
        'triggered_by': 'str',
        'updated_at': 'datetime'
    }

    attribute_map = {
        'config_file_path': 'config_file_path',
        'created_at': 'created_at',
        'created_by': 'created_by',
        'entity_id': 'entity_id',
        'entity_number': 'entity_number',
        'environment_id': 'environment_id',
        'id': 'id',
        'metrics': 'metrics',
        'model_artefact_id': 'model_artefact_id',
        'object': 'object',
        'pipeline_id': 'pipeline_id',
        'schedule_number': 'schedule_number',
        'script_parameters': 'script_parameters',
        'secrets': 'secrets',
        'source': 'source',
        'status': 'status',
        'triggered_by': 'triggered_by',
        'updated_at': 'updated_at'
    }

    readonly_attributes = {
        'created_at',
        'created_by',
        'entity_id',
        'entity_number',
        'metrics',
        'model_artefact_id',
        'object',
        'pipeline_id',
        'schedule_number',
        'triggered_by',
        'updated_at'
    }

    def __init__(self, config_file_path=None, created_at=None, created_by=None, entity_id=None, entity_number=None, environment_id=None, id=None, metrics=None, model_artefact_id=None, object='trainingPipelineRun', pipeline_id=None, schedule_number=None, script_parameters=None, secrets=None, source=None, status=None, triggered_by=None, updated_at=None, **kwargs):  # noqa: E501
        """TrainingPipelineRunSchema - a model defined in OpenAPI"""  # noqa: E501

        self._config_file_path = None
        self._created_at = None
        self._created_by = None
        self._entity_id = None
        self._entity_number = None
        self._environment_id = None
        self._id = None
        self._metrics = None
        self._model_artefact_id = None
        self._object = None
        self._pipeline_id = None
        self._schedule_number = None
        self._script_parameters = None
        self._secrets = None
        self._source = None
        self._status = None
        self._triggered_by = None
        self._updated_at = None
        self.discriminator = None

        if config_file_path is not None:
            self.config_file_path = config_file_path
        self.environment_id = environment_id
        if id is not None:
            self.id = id
        if script_parameters is not None:
            self.script_parameters = script_parameters
        if secrets is not None:
            self.secrets = secrets
        if source is not None:
            self.source = source
        if status is not None:
            self.status = status

    @classmethod
    def from_response(cls, config_file_path=None, created_at=None, created_by=None, entity_id=None, entity_number=None, environment_id=None, id=None, metrics=None, model_artefact_id=None, object='trainingPipelineRun', pipeline_id=None, schedule_number=None, script_parameters=None, secrets=None, source=None, status=None, triggered_by=None, updated_at=None, **kwargs):  # noqa: E501
        """Instantiate TrainingPipelineRunSchema from response"""  # noqa: E501
        self = cls.__new__(cls)

        self._config_file_path = None
        self._created_at = None
        self._created_by = None
        self._entity_id = None
        self._entity_number = None
        self._environment_id = None
        self._id = None
        self._metrics = None
        self._model_artefact_id = None
        self._object = None
        self._pipeline_id = None
        self._schedule_number = None
        self._script_parameters = None
        self._secrets = None
        self._source = None
        self._status = None
        self._triggered_by = None
        self._updated_at = None
        self.discriminator = None

        if config_file_path is not None:
            self.config_file_path = config_file_path
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if entity_id is not None:
            self.entity_id = entity_id
        if entity_number is not None:
            self.entity_number = entity_number
        self.environment_id = environment_id
        if id is not None:
            self.id = id
        if metrics is not None:
            self.metrics = metrics
        self.model_artefact_id = model_artefact_id
        if object is not None:
            self.object = object
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if schedule_number is not None:
            self.schedule_number = schedule_number
        if script_parameters is not None:
            self.script_parameters = script_parameters
        if source is not None:
            self.source = source
        if status is not None:
            self.status = status
        self.triggered_by = triggered_by
        if updated_at is not None:
            self.updated_at = updated_at
        return self

    @property
    def config_file_path(self):
        """Gets the config_file_path of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The config_file_path of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._config_file_path

    @config_file_path.setter
    def config_file_path(self, config_file_path):
        """Sets the config_file_path of this TrainingPipelineRunSchema.


        :param config_file_path: The config_file_path of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """
        if config_file_path is not None and len(config_file_path) > 1000:
            raise ValueError("Invalid value for `config_file_path`, length must be less than or equal to `1000`")  # noqa: E501
        if config_file_path is not None and len(config_file_path) < 1:
            raise ValueError("Invalid value for `config_file_path`, length must be greater than or equal to `1`")  # noqa: E501

        self._config_file_path = config_file_path

    @property
    def created_at(self):
        """Gets the created_at of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The created_at of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this TrainingPipelineRunSchema.


        :param created_at: The created_at of this TrainingPipelineRunSchema.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The created_by of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: UserSchema
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this TrainingPipelineRunSchema.


        :param created_by: The created_by of this TrainingPipelineRunSchema.  # noqa: E501
        :type: UserSchema
        """

        self._created_by = created_by

    @property
    def entity_id(self):
        """Gets the entity_id of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The entity_id of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._entity_id

    @entity_id.setter
    def entity_id(self, entity_id):
        """Sets the entity_id of this TrainingPipelineRunSchema.


        :param entity_id: The entity_id of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._entity_id = entity_id

    @property
    def entity_number(self):
        """Gets the entity_number of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The entity_number of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: int
        """
        return self._entity_number

    @entity_number.setter
    def entity_number(self, entity_number):
        """Sets the entity_number of this TrainingPipelineRunSchema.


        :param entity_number: The entity_number of this TrainingPipelineRunSchema.  # noqa: E501
        :type: int
        """

        self._entity_number = entity_number

    @property
    def environment_id(self):
        """Gets the environment_id of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The environment_id of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._environment_id

    @environment_id.setter
    def environment_id(self, environment_id):
        """Sets the environment_id of this TrainingPipelineRunSchema.


        :param environment_id: The environment_id of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """
        if environment_id is None:
            raise ValueError("Invalid value for `environment_id`, must not be `None`")  # noqa: E501
        if environment_id is not None and not re.search(r'^([a-zA-Z0-9\-]+)$', environment_id):  # noqa: E501
            raise ValueError(r"Invalid value for `environment_id`, must be a follow pattern or equal to `/^([a-zA-Z0-9\-]+)$/`")  # noqa: E501

        self._environment_id = environment_id

    @property
    def id(self):
        """Gets the id of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The id of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TrainingPipelineRunSchema.


        :param id: The id of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def metrics(self):
        """Gets the metrics of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The metrics of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: object
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """Sets the metrics of this TrainingPipelineRunSchema.


        :param metrics: The metrics of this TrainingPipelineRunSchema.  # noqa: E501
        :type: object
        """

        self._metrics = metrics

    @property
    def model_artefact_id(self):
        """Gets the model_artefact_id of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The model_artefact_id of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._model_artefact_id

    @model_artefact_id.setter
    def model_artefact_id(self, model_artefact_id):
        """Sets the model_artefact_id of this TrainingPipelineRunSchema.


        :param model_artefact_id: The model_artefact_id of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._model_artefact_id = model_artefact_id

    @property
    def object(self):
        """Gets the object of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The object of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this TrainingPipelineRunSchema.


        :param object: The object of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The pipeline_id of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this TrainingPipelineRunSchema.


        :param pipeline_id: The pipeline_id of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._pipeline_id = pipeline_id

    @property
    def schedule_number(self):
        """Gets the schedule_number of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The schedule_number of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: int
        """
        return self._schedule_number

    @schedule_number.setter
    def schedule_number(self, schedule_number):
        """Sets the schedule_number of this TrainingPipelineRunSchema.


        :param schedule_number: The schedule_number of this TrainingPipelineRunSchema.  # noqa: E501
        :type: int
        """

        self._schedule_number = schedule_number

    @property
    def script_parameters(self):
        """Gets the script_parameters of this TrainingPipelineRunSchema.  # noqa: E501

        Object mapping parameter name to overridden value  # noqa: E501

        :return: The script_parameters of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: object
        """
        return self._script_parameters

    @script_parameters.setter
    def script_parameters(self, script_parameters):
        """Sets the script_parameters of this TrainingPipelineRunSchema.

        Object mapping parameter name to overridden value  # noqa: E501

        :param script_parameters: The script_parameters of this TrainingPipelineRunSchema.  # noqa: E501
        :type: object
        """

        self._script_parameters = script_parameters

    @property
    def secrets(self):
        """Gets the secrets of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The secrets of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: object
        """
        return self._secrets

    @secrets.setter
    def secrets(self, secrets):
        """Sets the secrets of this TrainingPipelineRunSchema.


        :param secrets: The secrets of this TrainingPipelineRunSchema.  # noqa: E501
        :type: object
        """

        self._secrets = secrets

    @property
    def source(self):
        """Gets the source of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The source of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: object
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this TrainingPipelineRunSchema.


        :param source: The source of this TrainingPipelineRunSchema.  # noqa: E501
        :type: object
        """

        self._source = source

    @property
    def status(self):
        """Gets the status of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The status of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TrainingPipelineRunSchema.


        :param status: The status of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """
        allowed_values = ["Accepted", "Rejected", "Queued", "Running", "Failed", "Succeeded", "Unknown", "Stopping", "Stopped"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def triggered_by(self):
        """Gets the triggered_by of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The triggered_by of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: str
        """
        return self._triggered_by

    @triggered_by.setter
    def triggered_by(self, triggered_by):
        """Sets the triggered_by of this TrainingPipelineRunSchema.


        :param triggered_by: The triggered_by of this TrainingPipelineRunSchema.  # noqa: E501
        :type: str
        """

        self._triggered_by = triggered_by

    @property
    def updated_at(self):
        """Gets the updated_at of this TrainingPipelineRunSchema.  # noqa: E501


        :return: The updated_at of this TrainingPipelineRunSchema.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this TrainingPipelineRunSchema.


        :param updated_at: The updated_at of this TrainingPipelineRunSchema.  # noqa: E501
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
        if not isinstance(other, TrainingPipelineRunSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
