class BaseModel:
    """A base class for representing a single object on the server."""

    id_attribute = "id"
    version_attribute = "version"

    def __init__(self, attrs=None, client=None, collection=None):
        """Model Constructor.

        Args:
            attrs (dict, optional): The raw representation of this object from the API
            client (APIClient, optional): A client pointing at the server that this object is on.
            collection (Collection, optional): The collection that this model is part of.
        """
        self.collection = collection
        self.client = client
        self.attrs = attrs
        if self.attrs is None:
            self.attrs = {}

    def __repr__(self):
        if self.version:
            return "<%s: %s_v%s>" % (
                self.__class__.__name__,
                self.id,
                self.version,
            )
        return "<%s: %s>" % (self.__class__.__name__, self.id)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.id == other.id
            and self.version == other.version
        )

    def __hash__(self):
        return hash(
            "%s:%s:%s" % (self.__class__.__name__, self.id, self.version)
        )

    @property
    def id(self):
        """The ID of the object."""
        return self.attrs.get(self.id_attribute)

    @property
    def version(self):
        """The version of the object."""
        return self.attrs.get(self.version_attribute)

    def reload(self):
        """Load this object from the server.

        Again and update ``attrs`` with the new data.
        """
        new_model = self.collection.get(self.id, version_number=self.version)
        self.attrs = new_model.attrs


class BaseCollection:
    """A base class for representing all objects on the server."""

    # The type of object this collection represents, set by subclasses
    model = BaseModel

    def __init__(self, client=None, parent=None):
        #: The client pointing at the server that this collection of objects
        #: is on.
        self.client = client
        self.parent = parent

    def list(self):
        raise NotImplementedError

    def get(self, key, version_number=None):
        raise NotImplementedError

    def create(self, attrs=None):
        raise NotImplementedError

    def prepare_model(self, attrs):
        """Create a model from a set of attributes."""
        if isinstance(attrs, BaseModel):
            attrs.client = self.client
            attrs.collection = self
            return attrs
        if isinstance(attrs, dict):
            return self.model(attrs=attrs, client=self.client, collection=self)

        raise Exception(
            "Can't create %s from %s" % (self.model.__name__, attrs)
        )
