import logging
from google.cloud import storage

from mlflow.utils.qubole_object_store_utils import QuboleObjectStoreUtils

_logger = logging.getLogger(__name__)


class QuboleGCSUtils(QuboleObjectStoreUtils):
    URI_SCHEME = 'gs'

    def __init__(self):
        self.client = storage.Client()

    @classmethod
    def in_context(cls, uri_schema):
        return cls.URI_SCHEME == uri_schema

    def get_object_last_modified_time(self, bucket, key):
        try:
            connection = self.client.bucket(bucket)
            return connection.get_blob(key).updated.timestamp()
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(e)
            return None

    def copy_blob(self, source_bucket, source_key, destination_bucket, destination_key):
        source_connection = self.client.bucket(source_bucket)
        if source_bucket == destination_bucket:
            destination_connection = source_connection
        else:
            destination_connection = self.client.bucket(destination_bucket)
        source_blob = source_connection.blob(source_key)
        source_connection.copy_blob(source_blob, destination_connection, destination_key)
