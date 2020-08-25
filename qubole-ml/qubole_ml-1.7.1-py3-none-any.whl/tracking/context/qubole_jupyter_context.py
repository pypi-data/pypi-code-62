import logging
from abc import ABCMeta, abstractmethod

from mlflow.tracking.context.abstract_context import RunContextProvider
from mlflow.utils.qubole_metrics_events import (
    CLIENT_START_RUN,
    CLIENT_END_RUN,
    CLIENT_CREATE_EXPERIMENT,
    CLIENT_LOG_ARTIFACT
)
from mlflow.utils.qubole_metrics_utils import QuboleMetricsUtils
from mlflow.utils.qubole_utils import (
    is_auto_snapshot_enabled,
    is_jupyter_virtual_foldering_enabled
)

_logger = logging.getLogger(__name__)


class QuboleJupyterContext(RunContextProvider):
    __metaclass__ = ABCMeta

    def in_context(self):
        return (
            is_jupyter_virtual_foldering_enabled()
            and self.utils
            and self.utils.in_context()
        )

    @property
    @abstractmethod
    def _get_utils_class(self):
        raise NotImplementedError

    # pylint: disable=attribute-defined-outside-init, access-member-before-definition
    @property
    def utils(self):
        if hasattr(self, "__utils__"):
            return self.__utils__
        try:
            self.__utils__ = self._get_utils_class()
        except NotImplementedError:
            self.__utils__ = None
        return self.__utils__

    def pre_start_run_actions(self):
        try:
            if is_auto_snapshot_enabled():
                self.utils.create_snapshot()
        except Exception as e:  # pylint: disable=broad-except
            _logger.error("Could not successfully initialize run in Qubole context."
                          "Got error: %s", e)

    def post_start_run_actions(self, run):
        self.utils.send_start_run_event()
        _logger.debug("Sending start run event to Mojave.")
        QuboleMetricsUtils.send_event(
            CLIENT_START_RUN,
            run.to_dictionary())

    def post_end_run_actions(self, run_id, status):
        _logger.debug("Sending end run event to Mojave.")
        QuboleMetricsUtils.send_event(
            CLIENT_END_RUN,
            {
                "run_id": run_id,
                "status": status
            })

    def post_log_artifact_actions(self, local_path, artifact_path):
        _logger.debug("Sending log artifact event to Mojave.")
        QuboleMetricsUtils.send_event(
            CLIENT_LOG_ARTIFACT,
            {
                "local_path": local_path,
                "artifact_path": artifact_path
            })

    def post_create_experiment_actions(self, experiment):
        _logger.debug("Sending create experiment event to Mojave.")
        QuboleMetricsUtils.send_event(
            CLIENT_CREATE_EXPERIMENT,
            experiment.to_dictionary())

    def tags(self):
        return self.utils.get_tags()
