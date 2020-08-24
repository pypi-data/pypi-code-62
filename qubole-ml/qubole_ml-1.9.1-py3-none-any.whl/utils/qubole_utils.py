"""
This file contains top-level qubole specific utility functions
"""
import os
import pkg_resources
import re
import threading

from mlflow.utils.qubole_nodeinfo import NodeInfo

QUBOLE_PACKAGES_DIR = "/usr/lib/qubole"
QUBOLE_MLFLOW_TRACKING_URI_REGEX = \
    r"https://([\w.-]+)\.qubole\.(com|net)/([\w-]+)?mlflow-tracking-(\w+)"

##################################################################
# Misc Utiliy functions
##################################################################


def is_empty(x):
    """
    Checks if a string is not empty
    :return: :py:class:`bool`
    """
    return not x or x == ''


def get_property_from_spark_context(key):
    try:
        from pyspark import SparkContext  # pylint: disable=import-error
        spark_context = SparkContext._active_spark_context
        return spark_context.getLocalProperty(key)
    except Exception:  # pylint: disable=broad-except
        try:
            from pyspark import TaskContext  # pylint: disable=import-error
            task_context = TaskContext.get()
            return task_context.getLocalProperty(key)
        except Exception:  # pylint: disable=broad-except
            return None


def get_spark_application_id():
    try:
        from pyspark import SparkContext  # pylint: disable=import-error
        spark_context = SparkContext._active_spark_context
        return spark_context.applicationId
    except Exception:  # pylint: disable=broad-except
        return None


def run_in_daemon_thread(func):
    class __QuboleBackgroundThread__(object):
        def __init__(self):
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()

        def run(self):
            func()

    __QuboleBackgroundThread__()


def format_dict(d):
    return {str(x): str(y) for x, y in d.items() if not is_empty(y)}


##################################################################
# Qubole context related functions
##################################################################


def is_running_in_qubole():
    """
    Checks if the client is running in Qubole cluster
    :return: :py:class:`bool`
    """
    return os.path.isdir(QUBOLE_PACKAGES_DIR)


def get_mlflow_version():
    return (
        pkg_resources
        .get_distribution(
            "qubole-ml"
        ).version)


def is_qubole_tracking_uri(uri):
    """
    Checks if the given URI is qubole tracking URI
    :return: :py:class:`bool`
    """
    pattern = re.compile(QUBOLE_MLFLOW_TRACKING_URI_REGEX)
    return pattern.search(uri)


##################################################################
# NodeInfo related functions
##################################################################


def get_defloc():
    """
    Gets customer defloc path from nodeinfo
    :return: :py:class:`str` customer defloc path.
    """
    if NodeInfo.get_info("s3_default_location"):
        return NodeInfo.get_info("s3_default_location")
    else:
        return NodeInfo.get_info("default_location")


def is_jupyter_virtual_foldering_enabled():
    """
    Gets customer defloc path from nodeinfo
    :return: :py:class:`str` customer defloc path.
    """
    return NodeInfo.get_feature("jupy.virtual_foldering")


def get_aws_keys():
    if NodeInfo.get_info("s3_access_key_id"):
        return NodeInfo.get_info("s3_access_key_id"), \
               NodeInfo.get_info("s3_secret_access_key")
    elif NodeInfo.get_info("aws_access_key"):
        return NodeInfo.get_info("aws_access_key"), \
               NodeInfo.get_info("aws_secret_key")
    else:
        return None, None


def is_auto_snapshot_enabled():
    return NodeInfo.get_feature("ds.use_mlflow_auto_snapshot")


def get_master_dns():
    if NodeInfo.get_feature("hadoop.private_ip") and \
       NodeInfo.get_feature("spark.private_ip"):
        return NodeInfo.get_info("master_ip")
    else:
        return NodeInfo.get_info("master_public_dns_or_private_ip")


def get_cluster_type():
    if NodeInfo.get_info("use_mlflow") == "1":
        return "mlflow"
    else:
        return "spark"


def get_qubole_base_uri():
    return NodeInfo.get_info("qubole_base_url")


def is_metrics_enabled():
    return NodeInfo.get_feature("mojave.enable_metricsd") and \
           NodeInfo.get_feature("ds.use_mlflow_metrics_logging")


def get_cluster_id():
    return NodeInfo.get_info("cluster_id")


def get_cluster_inst_id():
    return NodeInfo.get_info("cluster_inst_id")


def get_cluster_spark_version():
    return NodeInfo.get_info("spark_version")


def get_cluster_auth_token():
    return NodeInfo.get_info("qubole_cluster_api_token")


def get_asterix_auth_token():
    return NodeInfo.get_info("qubole_asterix_api_token")


def get_runtime_id():
    return NodeInfo.get_info("runtime_id")


def get_quboled_env_id():
    return NodeInfo.get_info("quboled_env_id")
