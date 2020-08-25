import re

from mlflow.utils.mlflow_tags import (
    MLFLOW_QUBOLE_CLUSTER_ID,
    MLFLOW_QUBOLE_CLUSTER_INST_ID,
    MLFLOW_QUBOLE_QUBOLED_ENV_ID,
    MLFLOW_QUBOLE_SPARK_APPLICATION_ID,
    MLFLOW_QUBOLE_SPARK_VERSION
)
from mlflow.utils.qubole_jupyter_utils import QuboleJupyterUtils
from mlflow.utils.qubole_utils import (
    format_dict,
    get_cluster_auth_token,
    get_cluster_id,
    get_cluster_inst_id,
    get_cluster_spark_version,
    get_master_dns,
    get_property_from_spark_context,
    get_quboled_env_id,
    get_spark_application_id
)

QUBOLE_MLFLOW_OPS_TUNNEL_TRACKING_URI_PATH = "ops-tunnel-mlflow-tracking-default"
QUBOLE_MLFLOW_SPARK_JOB_PROPERTY_VAR = "spark.job.description"
QUBOLE_MLFLOW_CLUSTER_JUPYTER_SERVER_PORT = 8888
QUBOLE_MLFLOW_CLUSTER_JUPYTER_BASE_URI = "jupyter-notebook"
QUBOLE_MLFLOW_SPARK_JOB_KERNEL_ID_REGEX = r".*Kernel Id: (\w+-\w+-\w+-\w+-\w+).*"


class QubolePySparkUtils(QuboleJupyterUtils):
    @property
    def _tracking_uri_path(self):
        return QUBOLE_MLFLOW_OPS_TUNNEL_TRACKING_URI_PATH

    @property
    def _jupyter_hostname(self):
        return "http://{}:{}".format(
            get_master_dns(),
            QUBOLE_MLFLOW_CLUSTER_JUPYTER_SERVER_PORT
        )

    @property
    def _jupyter_base_uri(self):
        return "{}-{}".format(
            QUBOLE_MLFLOW_CLUSTER_JUPYTER_BASE_URI,
            get_cluster_id()
        )

    def _get_kernel_id(self):
        """
        Fetched Qubole configuration from Spark Context and returns it as a dictionary
        :return: :py:class:`dict`
        """
        try:
            job_description = get_property_from_spark_context(
                QUBOLE_MLFLOW_SPARK_JOB_PROPERTY_VAR
            )
            pattern = re.compile(QUBOLE_MLFLOW_SPARK_JOB_KERNEL_ID_REGEX)
            return pattern.match(job_description).group(1)
        except Exception:  # pylint: disable=broad-except
            return None

    def _get_auth_token(self):
        return get_cluster_auth_token()

    def _get_cluster_tags(self):
        return format_dict({
            MLFLOW_QUBOLE_CLUSTER_ID: get_cluster_id(),
            MLFLOW_QUBOLE_CLUSTER_INST_ID: get_cluster_inst_id(),
            MLFLOW_QUBOLE_SPARK_VERSION: get_cluster_spark_version(),
            MLFLOW_QUBOLE_QUBOLED_ENV_ID: get_quboled_env_id(),
            MLFLOW_QUBOLE_SPARK_APPLICATION_ID: get_spark_application_id()
        })

    def get_tags(self):
        cluster_tags = self._get_cluster_tags()
        parent_tags = super(QubolePySparkUtils, self).get_tags()
        return {
            **cluster_tags,
            **parent_tags
        }
