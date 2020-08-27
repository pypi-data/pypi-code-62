from cral.tracking.entities.model_registry import RegisteredModel
from cral.tracking.entities.model_registry._model_registry_entity import _ModelRegistryEntity
from cral.tracking.protos.model_registry_pb2 import ModelVersion as ProtoModelVersion


class ModelVersion(_ModelRegistryEntity):
    """
    .. note::
        Experimental: This entity may change or be removed in a future release without warning.

    MLflow entity for Model Version.
    A model version is uniquely identified using underlying
    :py:class:`cral.tracking.entities.model_registry.RegisteredModel` and version number.
    """
    def __init__(self, registered_model, version):
        """
        Construct a :py:class:`cral.tracking.entities.model_registry.RegisteredModel` instance
        :param registered_model: Is an instance of
                                 :py:class:`cral.tracking.entities.model_registry.RegisteredModel`
        :param version: Integer version
        """
        super(ModelVersion, self).__init__()
        self._registered_model = registered_model
        self._version = version

    @property
    def registered_model(self):
        """An instance of :py:class:`cral.tracking.entities.model_registry.RegisteredModel`"""
        return self._registered_model

    def get_name(self):
        """String. Unique name within Model Registry."""
        return self.registered_model.name

    @property
    def version(self):
        """Integer version number"""
        return self._version

    # proto mappers
    @classmethod
    def from_proto(cls, proto):
        # input: cral.tracking.protos.model_registry_pb2.ModelVersion
        # returns: ModelVersion entity
        return cls(RegisteredModel.from_proto(proto.registered_model), proto.version)

    def to_proto(self):
        # returns cral.tracking.protos.model_registry_pb2.ModelVersion
        model_version = ProtoModelVersion()
        model_version.registered_model.MergeFrom(self.registered_model.to_proto())
        model_version.version = self.version
        return model_version
