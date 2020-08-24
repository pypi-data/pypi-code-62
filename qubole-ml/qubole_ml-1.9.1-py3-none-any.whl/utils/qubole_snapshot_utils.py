import logging
import sys
import time
import traceback
import uuid

from mlflow.utils.qubole_metrics_events import (
    CLIENT_CREATE_SNAPSHOT,
    CLIENT_SNAPSHOT_CREATION_ERROR
)
from mlflow.utils.qubole_metrics_utils import QuboleMetricsUtils
from mlflow.utils.qubole_utils import (
    get_defloc,
    run_in_daemon_thread
)
from mlflow.utils.uri import get_uri_scheme
from mlflow.utils.qubole_object_store_utils_factory import QuboleObjectStoreUtilsFactory

NOTEBOOK_KEY_PREFIX = "jupyter/notebooks"
SNAPSHOT_KEY_PREFIX = "mlflow/snapshots"
MIN_SNAPSHOT_FRESHNESS = 5
MAX_SNAPSHOT_RETRIES = 10
SNAPSHOT_RETRY_INTERVAL = 2


_logger = logging.getLogger(__name__)


class QuboleSnapshotUtils(object):
    def __init__(self, notebook_path, notebook_id):
        self.notebook_path = notebook_path
        self.notebook_id = notebook_id
        self.uri_scheme = get_uri_scheme(get_defloc())

        self.snapshot_path = None
        self.jupyter_snapshot_path = None

    # pylint: disable=attribute-defined-outside-init, access-member-before-definition
    @property
    def cloud_utils(self):
        if hasattr(self, "__cloud_utils__"):
            return self.__cloud_utils__
        self.__cloud_utils__ = QuboleObjectStoreUtilsFactory.get_utils(self.uri_scheme)
        return self.__cloud_utils__

    def get_snapshot_path(self):
        return self.snapshot_path

    def get_jupyter_snapshot_path(self):
        return self.jupyter_snapshot_path

    def _get_object_last_modified_time(self, bucket, key):
        return self.cloud_utils.get_object_last_modified_time(bucket, key)

    def _split_defloc_path(self, defloc):
        defloc = defloc.split("{}://".format(self.uri_scheme))[1].split("/")
        return defloc[0], "/".join(defloc[1:]).rstrip("/")

    def _get_path_for_notebook(self):
        return "{0}/{1}/{1}.ipynb".format(NOTEBOOK_KEY_PREFIX, self.notebook_id)

    def _generate_snapshot_key(self):
        return "{}/{}.ipynb".format(SNAPSHOT_KEY_PREFIX, str(uuid.uuid4()))

    def _copy_notebook(self, bucket, notebook_key, snapshot_key):
        self.cloud_utils.copy_blob(bucket, notebook_key, bucket, snapshot_key)

    def _wait_and_create_snapshot(self, bucket, notebook_key, snapshot_key):
        _logger = logging.getLogger("qubole_snapshot_util_worker_thread")

        start_time = time.time()

        min_modified_time = time.time() - MIN_SNAPSHOT_FRESHNESS
        num_retries = 0

        while num_retries < MAX_SNAPSHOT_RETRIES:
            last_modified = self._get_object_last_modified_time(bucket, notebook_key)
            if last_modified >= min_modified_time:
                break
            time.sleep(SNAPSHOT_RETRY_INTERVAL)

        try:
            self._copy_notebook(bucket, notebook_key, snapshot_key)

            time_taken = time.time() - start_time

            QuboleMetricsUtils.send_event(
                CLIENT_CREATE_SNAPSHOT,
                {
                    "bucket": bucket,
                    "notebook_key": notebook_key,
                    "snapshot_key": snapshot_key,
                    "time_taken": time_taken
                })
            _logger.info(
                "Successfully created snapshot for notebook %s at %s",
                notebook_key,
                snapshot_key
                )
        except Exception as e:  # pylint: disable=broad-except
            QuboleMetricsUtils.send_event(
                CLIENT_SNAPSHOT_CREATION_ERROR,
                {
                    "bucket": bucket,
                    "notebook_key": notebook_key,
                    "snapshot_key": snapshot_key,
                    "exception": getattr(e, 'message', repr(e)),
                    "backtrace": traceback.format_tb(sys.exc_info()[2])
                })

            _logger.error("Failed to create notebook snapshot. Failed with error: %s", e)

    def create_snapshot(self):
        defloc = get_defloc()
        bucket, base_key = self._split_defloc_path(defloc)
        notebook_key = "{}/{}".format(base_key, self._get_path_for_notebook())
        relative_snapshot_key = self._generate_snapshot_key()
        snapshot_key = "{}/{}".format(base_key, relative_snapshot_key)

        def create_snapshot():
            return self._wait_and_create_snapshot(
                bucket,
                notebook_key,
                snapshot_key)

        run_in_daemon_thread(create_snapshot)

        self.snapshot_path = "{}://{}/{}".format(self.uri_scheme, bucket, snapshot_key)
        self.jupyter_snapshot_path = "_root/{}".format(relative_snapshot_key)

        return self.snapshot_path, self.jupyter_snapshot_path
