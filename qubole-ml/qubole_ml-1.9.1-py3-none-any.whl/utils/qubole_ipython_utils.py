import re

from mlflow.utils.mlflow_tags import MLFLOW_QUBOLE_RUNTIME_ID
from mlflow.utils.qubole_jupyter_utils import QuboleJupyterUtils
from mlflow.utils.qubole_utils import (
    format_dict,
    get_asterix_auth_token,
    get_runtime_id
)

QUBOLE_MLFLOW_ASTERIX_TUNNEL_TRACKING_URI_PATH = "asterix-ops-tunnel-mlflow-tracking-default"
QUBOLE_MLFLOW_RUNTIME_JUPYTER_SERVER_IP = "localhost"
QUBOLE_MLFLOW_RUNTIME_JUPYTER_SERVER_PORT = 8888
QUBOLE_MLFLOW_RUNTIME_JUPYTER_BASE_URI = "jupyter-runtime"
QUBOLE_MLFLOW_IPYTHON_KERNEL_ID_REGEX = r".*kernel-(\w+-\w+-\w+-\w+-\w+).json"


class QuboleIPythonUtils(QuboleJupyterUtils):
    @property
    def _tracking_uri_path(self):
        return QUBOLE_MLFLOW_ASTERIX_TUNNEL_TRACKING_URI_PATH

    @property
    def _jupyter_hostname(self):
        return "http://{}:{}".format(
            QUBOLE_MLFLOW_RUNTIME_JUPYTER_SERVER_IP,
            QUBOLE_MLFLOW_RUNTIME_JUPYTER_SERVER_PORT
        )

    @property
    def _jupyter_base_uri(self):
        return "{}/{}".format(
            QUBOLE_MLFLOW_RUNTIME_JUPYTER_BASE_URI,
            get_runtime_id()
        )

    def _get_kernel_id(self):
        """
        Fetched Qubole configuration from Spark Context and returns it as a dictionary
        :return: :py:class:`dict`
        """
        try:
            from IPython.lib import kernel
            connection_file_path = kernel.get_connection_file()
            pattern = re.compile(QUBOLE_MLFLOW_IPYTHON_KERNEL_ID_REGEX)
            return pattern.match(connection_file_path).group(1)
        except Exception:  # pylint: disable=broad-except
            return None

    def _get_auth_token(self):
        return get_asterix_auth_token()

    def _get_runtime_tags(self):
        return format_dict({
            MLFLOW_QUBOLE_RUNTIME_ID: get_runtime_id()
        })

    def get_tags(self):
        runtime_tags = self._get_runtime_tags()
        parent_tags = super(QuboleIPythonUtils, self).get_tags()
        return {
            **runtime_tags,
            **parent_tags
        }
