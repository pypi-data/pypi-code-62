import logging
import sys
import time
import traceback
import uuid
from abc import abstractmethod

from mlflow.entities import SourceType
from mlflow.utils.mlflow_tags import (
    MLFLOW_QUBOLE_JUPYTER_SNAPSHOT_PATH,
    MLFLOW_QUBOLE_NOTEBOOK_ID,
    MLFLOW_QUBOLE_NOTEBOOK_NAME,
    MLFLOW_QUBOLE_NOTEBOOK_PATH,
    MLFLOW_QUBOLE_SNAPSHOT_PATH,
    MLFLOW_QUBOLE_USER_EMAIL,
    MLFLOW_SOURCE_NAME,
    MLFLOW_SOURCE_TYPE,
    MLFLOW_USER
)
from mlflow.utils.rest_utils import http_request, MlflowHostCreds
from mlflow.utils.qubole_context_utils import QuboleContextUtils
from mlflow.utils.qubole_metrics_events import (
    CLIENT_GET_KERNEL_INFO,
    CLIENT_GET_KERNEL_INFO_ERROR,
    CLIENT_PUT_KERNEL_MESSAGE,
    CLIENT_PUT_KERNEL_MESSAGE_ERROR
)
from mlflow.utils.qubole_metrics_utils import QuboleMetricsUtils
from mlflow.utils.qubole_utils import format_dict
from mlflow.utils.qubole_snapshot_utils import QuboleSnapshotUtils

QUBOLE_MLFLOW_JUPYTER_KERNEL_INFO_URI_TEMPLATE = "qubole/api/v1/kernel/{}/info"
QUBOLE_MLFLOW_JUPYTER_KERNEL_MESSAGE_URI_TEMPLATE = "qubole/api/v1/kernel/{}/message"
QUBOLE_MLFLOW_JUPYTER_START_RUN_EVENT = "mlflow.run.start"
QUBOLE_MLFLOW_JUPYTER_SAVE_NOTEBOOK = "mlflow.notebook.save"

_logger = logging.getLogger(__name__)


class QuboleJupyterUtils(QuboleContextUtils):
    def in_context(self):
        return self._get_kernel_id() is not None

    @property
    @abstractmethod
    def _jupyter_hostname(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _jupyter_base_uri(self):
        raise NotImplementedError

    # pylint: disable=attribute-defined-outside-init, access-member-before-definition
    @property
    def snapshot_utils(self):
        if hasattr(self, "__snapshot_utils__"):
            return self.__snapshot_utils__
        try:
            notebook_details = self._get_notebook_details()
            self.__snapshot_utils__ = \
                QuboleSnapshotUtils(
                    notebook_details["notebook_path"],
                    notebook_details["notebook_id"]
                )
            return self.__snapshot_utils__
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(e)
            return None

    @abstractmethod
    def _get_kernel_id(self):
        raise NotImplementedError

    # pylint: disable=attribute-defined-outside-init, access-member-before-definition
    def _get_notebook_details(self):
        """
        Makes a call to jupyter server to fetch information about notebook based on kernel id
        :return: :py:class:`dict` Containing infomation about the notebook
        """
        if hasattr(self, "__note_details__"):
            return self.__note_details__
        try:
            start_time = time.time()
            response = http_request(
                        self._get_jupyter_host_creds(),
                        self._get_jupyter_kernel_info_api_path(),
                        method="GET")

            time_taken = time.time() - start_time

            QuboleMetricsUtils.send_event(
                CLIENT_GET_KERNEL_INFO,
                {
                    "kernel_id": self._get_kernel_id(),
                    "time_taken": time_taken
                })

            self.__note_details__ = response.json()
        except Exception as e:  # pylint: disable=broad-except
            QuboleMetricsUtils.send_event(
                CLIENT_GET_KERNEL_INFO_ERROR,
                {
                    "kernel_id": self._get_kernel_id(),
                    "exception": getattr(e, 'message', repr(e)),
                    "backtrace": traceback.format_tb(sys.exc_info()[2])
                })
            print("\x1b[31mCould not resolve notebook details. "
                  "Please restart the kernel and try again.\n"
                  "If the issue persists reach out to Qubole support.\x1b[0m")
            self.__note_details__ = None

        return self.__note_details__

    def _send_event(self, event_type, message):
        """
        Makes a call to jupyter server to fetch information about notebook based on kernel id
        :return: :py:class:`dict` Containing infomation about the notebook
        """
        try:
            params = {
                "event_name": event_type,
                "message": message if message else "none"
            }

            start_time = time.time()

            response = http_request(
                        self._get_jupyter_host_creds(),
                        self._get_jupyter_kernel_message_api_path(),
                        method="PUT",
                        params=params)

            time_taken = time.time() - start_time

            QuboleMetricsUtils.send_event(
                CLIENT_PUT_KERNEL_MESSAGE,
                {
                    "kernel_id": self._get_kernel_id(),
                    "event_type": event_type,
                    "message": message,
                    "time_taken": time_taken
                })

            return response.json()
        except Exception as e:  # pylint: disable=broad-except
            QuboleMetricsUtils.send_event(
                CLIENT_PUT_KERNEL_MESSAGE_ERROR,
                {
                    "kernel_id": self._get_kernel_id(),
                    "exception": getattr(e, 'message', repr(e)),
                    "backtrace": traceback.format_tb(sys.exc_info()[2])
                })
            return None

    def _get_jupyter_host_creds(self):
        xsrf_token = str(uuid.uuid4())
        return MlflowHostCreds(
            self._jupyter_hostname,
            xsrf_token=xsrf_token,
            cookie="_xsrf={}".format(xsrf_token)
        )

    def _get_jupyter_uri(self, uri):
        return "/{}/{}".format(self._jupyter_base_uri, uri)

    def _get_jupyter_kernel_info_api_path(self):
        return self._get_jupyter_uri(
            QUBOLE_MLFLOW_JUPYTER_KERNEL_INFO_URI_TEMPLATE.format(
                self._get_kernel_id()
            )
        )

    def _get_jupyter_kernel_message_api_path(self):
        return self._get_jupyter_uri(
            QUBOLE_MLFLOW_JUPYTER_KERNEL_MESSAGE_URI_TEMPLATE.format(
                self._get_kernel_id()
            )
        )

    def send_start_run_event(self):
        self._send_event(QUBOLE_MLFLOW_JUPYTER_START_RUN_EVENT, None)

    def _send_save_notebook_event(self):
        self._send_event(QUBOLE_MLFLOW_JUPYTER_SAVE_NOTEBOOK, None)

    def create_snapshot(self):
        try:
            self._send_save_notebook_event()
            self.snapshot_utils.create_snapshot()
        except Exception:  # pylint: disable=broad-except
            print("\x1b[31mCould not create notebook snapshot. "
                  "Please try again and if the issue persists "
                  "reach out to Qubole support.\x1b[0m")

    def _get_snapshot_tags(self):
        try:
            return format_dict({
                MLFLOW_QUBOLE_SNAPSHOT_PATH: self.snapshot_utils.get_snapshot_path(),
                MLFLOW_QUBOLE_JUPYTER_SNAPSHOT_PATH: self.snapshot_utils.get_jupyter_snapshot_path()
            })
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(e)
            return {}

    def _get_notebook_tags(self):
        notebook_details = self._get_notebook_details()
        try:
            return format_dict({
                MLFLOW_QUBOLE_NOTEBOOK_ID: notebook_details["notebook_id"],
                MLFLOW_QUBOLE_NOTEBOOK_NAME: notebook_details["notebook_name"],
                MLFLOW_QUBOLE_NOTEBOOK_PATH: notebook_details["notebook_path"],
                MLFLOW_QUBOLE_USER_EMAIL: notebook_details["user"],
                MLFLOW_SOURCE_NAME: notebook_details["notebook_name"],
                MLFLOW_SOURCE_TYPE: SourceType.to_string(SourceType.NOTEBOOK),
                MLFLOW_USER: notebook_details["user"].split("@")[0]
            })
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(e)
            return {}

    def get_tags(self):
        notebook_tags = self._get_notebook_tags()
        snapshot_tags = self._get_snapshot_tags()
        parent_tags = super(QuboleJupyterUtils, self).get_tags()
        return {
            **notebook_tags,
            **snapshot_tags,
            **parent_tags
        }
