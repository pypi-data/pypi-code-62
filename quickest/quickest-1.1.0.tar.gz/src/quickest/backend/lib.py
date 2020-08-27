import os, json, logging
from datetime import datetime


class Serialiser:
    """Interface for saving and loading to disk, db etc
    """

    def save(self, *args, **kwargs):
        raise NotImplementedError

    def load(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def opts(self, *args, **kwargs):
        # Get a list of config options
        raise NotImplementedError


class Disk(Serialiser):
    def __init__(self, loc=None):
        if loc is None:
            self._loc = os.getcwd()
        else:
            self._loc = loc

    def save(self, data, filename=None, **kwargs):

        if filename is None:
            now = datetime.now()
            filename = now.strftime("%Y%m%d_%H%M%S_%f")

        filename_with_ext = os.path.join(self._loc, filename + ".json")

        with open(filename_with_ext, "w") as outfile:
            json.dump(data, outfile)

        logging.info("Data written to file {}".format(filename_with_ext))

    def load(self, *args, **kwargs):
        pass

    @staticmethod
    def opts():
        return [{"kwarg": "loc", "description": "Where to save data"}]


class Mongo(Serialiser):
    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    @staticmethod
    def opts():
        # Get a list of config options
        return [
            {"kwarg": "username", "description": "MongoDB user"},
            {"kwarg": "password", "description": "MongoDB password"},
            {"kwarg": "host", "description": "where the MongoDB client is running"},
        ]


class Backend:
    def __init__(self, type="disk", **kwargs):

        if type == "disk":
            self._serialiser = Disk(**kwargs)
        else:
            raise AttributeError("No backend type {}".format(type))

    def save(self, data, **kwargs):

        self._serialiser.save(data, **kwargs)

    @staticmethod
    def get_opts():
        return {"disk": Disk.opts(), "mongo": Mongo.opts()}

