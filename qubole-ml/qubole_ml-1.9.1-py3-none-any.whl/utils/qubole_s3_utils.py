import logging
from mlflow.utils.boto_utils import get_client

from mlflow.utils.qubole_object_store_utils import QuboleObjectStoreUtils

_logger = logging.getLogger(__name__)


class QuboleS3Utils(QuboleObjectStoreUtils):
    URI_SCHEME = 's3'

    def __init__(self):
        self.client = get_client("s3")

    @classmethod
    def in_context(cls, uri_scheme):
        return cls.URI_SCHEME == uri_scheme

    def get_object_last_modified_time(self, bucket, key):
        try:
            return self.client.head_object(Bucket=bucket, Key=key)["LastModified"].timestamp()
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(e)
            return None

    def copy_blob(self, source_bucket, source_key, destination_bucket, destination_key):
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        self.client.copy(copy_source, destination_bucket, destination_key)
