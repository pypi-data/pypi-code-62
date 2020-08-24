from abc import ABC, abstractmethod


class QuboleObjectStoreUtils(ABC):

    @abstractmethod
    def get_object_last_modified_time(self, bucket, key):
        raise NotImplementedError

    @abstractmethod
    def copy_blob(self, source_bucket, source_key, destination_bucket, destination_key):
        raise NotImplementedError
