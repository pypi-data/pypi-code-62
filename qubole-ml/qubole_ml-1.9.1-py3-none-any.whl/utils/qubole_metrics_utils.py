"""
This module implements the class handling the Mojave events.
"""
import json
import logging
import requests

from mlflow.utils.qubole_utils import (
    get_cluster_type,
    get_master_dns,
    get_mlflow_version,
    is_metrics_enabled,
    is_running_in_qubole,
    run_in_daemon_thread
)

QUBOLE_METRICSD_URI_TEMPLATE = "http://{}:11500/event?source={}"
QUBOLE_MLFLOW_METRICS_PREFIX = "CLUSTER.MLFLOW.EVENT"

_logger = logging.getLogger(__name__)


class QuboleMetricsUtils():
    """
    Utility to log metrics in Qubole clusters
    """
    @classmethod
    def _get_client_info(cls):
        return {
            "__mlflow_version__": get_mlflow_version(),
            "__cluster_type__": get_cluster_type()
        }

    @classmethod
    def _send_event_to_mojave(cls, event_type, event_data):
        """
        Sends event to metricsd on port 11500
        """
        _logger = logging.getLogger("qubole_metrics_util_worker_thread")

        uri = QUBOLE_METRICSD_URI_TEMPLATE.format(get_master_dns(), event_type)
        headers = {"Content-type": "application/octet-stream"}

        try:
            response = requests.request(
                                'POST',
                                uri,
                                data=json.dumps(event_data),
                                headers=headers)

            if response.status_code == 201:
                _logger.info(
                    "Successfully sent mojave event for %s", event_type)
            else:
                _logger.error(
                    "Error in sending event %s", response.reason)
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(
                "Exception sending event %s to mojave: %s", event_type, e)

    @classmethod
    def _send_event_to_mojave_in_background(cls, event_type, event_data):
        run_in_daemon_thread(
            lambda: cls._send_event_to_mojave(event_type, event_data))

    @classmethod
    def send_event(cls, event_type, event_data):
        try:
            if is_running_in_qubole() and \
               is_metrics_enabled():
                event_type = "{}.{}".format(
                    QUBOLE_MLFLOW_METRICS_PREFIX,
                    event_type)
                event_data.update(cls._get_client_info())

                cls._send_event_to_mojave_in_background(
                    event_type,
                    event_data)
        except Exception as e:  # pylint: disable=broad-except
            _logger.error(
                "Exception preparing event %s to mojave: %s", event_type, e)
