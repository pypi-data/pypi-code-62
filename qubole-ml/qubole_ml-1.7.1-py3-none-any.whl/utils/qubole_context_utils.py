import logging
from abc import ABC, abstractmethod

from mlflow.utils.rest_utils import http_request, MlflowHostCreds
from mlflow.utils.qubole_utils import get_qubole_base_uri

_logger = logging.getLogger(__name__)
_qubole_mlflow_cluster_down_message_printed = False


class QuboleContextUtils(ABC):
    @abstractmethod
    def in_context(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _tracking_uri_path(self):
        raise NotImplementedError

    @abstractmethod
    def _get_auth_token(self):
        raise NotImplementedError

    def get_tags(self):
        return {}

    def get_tracking_uri(self):
        """
        Returns tracking URI for Qubole context
        :return: :py:class:`string`
        """
        base_uri = get_qubole_base_uri()
        return "{}/{}".format(base_uri, self._tracking_uri_path)

    def is_qubole_tracking_server_available(self):
        global _qubole_mlflow_cluster_down_message_printed

        creds = self.get_qubole_host_creds(self.get_tracking_uri())

        try:
            response = http_request(
                        creds,
                        "/",
                        method="GET")
            if response.status_code == 200:
                return True
        except Exception:  # pylint: disable=broad-except
            pass

        if not _qubole_mlflow_cluster_down_message_printed:
            print("\x1b[31mQubole MLflow tracking server is inaccessible, "
                  "please make sure that your MLflow cluster is running.\n"
                  "Data logged during this session will not be accessible later.\x1b[0m")
            _qubole_mlflow_cluster_down_message_printed = True

        return False

    def get_qubole_host_creds(self, uri):
        """
        Finds HTTP credentials from nodeinfo and returns MlflowHostCreds class
        :return: :py:class:`mlflow.rest_utils.MlflowHostCreds` which includes the hostname and
            authentication information necessary to talk to the Qubole server.
        """
        return MlflowHostCreds(
            uri,
            x_auth_token=self._get_auth_token()
        )
