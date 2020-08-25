import entrypoints
import warnings

from mlflow.tracking.context.default_context import DefaultRunContext
from mlflow.tracking.context.git_context import GitRunContext
from mlflow.tracking.context.databricks_notebook_context import DatabricksNotebookRunContext
from mlflow.tracking.context.databricks_job_context import DatabricksJobRunContext
from mlflow.tracking.context.qubole_pyspark_context import QubolePySparkContext
from mlflow.tracking.context.qubole_ipython_context import QuboleIPythonContext


class RunContextProviderRegistry(object):
    """Registry for run context provider implementations

    This class allows the registration of a run context provider which can be used to infer meta
    information about the context of an MLflow experiment run. Implementations declared though the
    entrypoints `mlflow.run_context_provider` group can be automatically registered through the
    `register_entrypoints` method.

    Registered run context providers can return tags that override those implemented in the core
    library, however the order in which plugins are resolved is undefined.
    """

    def __init__(self):
        self._registry = []

    def register(self, run_context_provider_cls):
        self._registry.append(run_context_provider_cls())

    def register_entrypoints(self):
        """Register tracking stores provided by other packages"""
        for entrypoint in entrypoints.get_group_all("mlflow.run_context_provider"):
            try:
                self.register(entrypoint.load())
            except (AttributeError, ImportError) as exc:
                warnings.warn(
                    'Failure attempting to register context provider "{}": {}'.format(
                        entrypoint.name, str(exc)
                    ),
                    stacklevel=2
                )

    def __iter__(self):
        return iter(self._registry)


_run_context_provider_registry = RunContextProviderRegistry()
_run_context_provider_registry.register(DefaultRunContext)
_run_context_provider_registry.register(GitRunContext)
_run_context_provider_registry.register(DatabricksNotebookRunContext)
_run_context_provider_registry.register(DatabricksJobRunContext)
_run_context_provider_registry.register(QubolePySparkContext)
_run_context_provider_registry.register(QuboleIPythonContext)

_run_context_provider_registry.register_entrypoints()


def resolve_tags(tags=None):
    """Generate a set of tags for the current run context. Tags are resolved in the order,
    contexts are registered. Argument tags are applied last.

    This function iterates through all run context providers in the registry. Additional context
    providers can be registered as described in
    :py:class:`mlflow.tracking.context.RunContextProvider`.

    :param tags: A dictionary of tags to override. If specified, tags passed in this argument will
                 override those inferred from the context.
    :return: A dicitonary of resolved tags.
    """

    all_tags = {}
    for provider in _run_context_provider_registry:
        if provider.in_context():
            # TODO: Error out gracefully if provider's tags are not valid or have wrong types.
            all_tags.update(provider.tags())

    if tags is not None:
        all_tags.update(tags)

    return all_tags


def _run_function_if_in_context(f):
    for provider in _run_context_provider_registry:
        if provider.in_context():
            try:
                f(provider)
            except Exception:  # pylint: disable=broad-except
                pass


def pre_start_run_actions():
    """
    Does context specific pre-start actions
    :return: None
    """
    _run_function_if_in_context(
        lambda x: x.pre_start_run_actions())


def post_start_run_actions(run):
    """
    Does context specific post-start actions
    :return: None
    """
    _run_function_if_in_context(
        lambda x: x.post_start_run_actions(run))


def post_end_run_actions(run_id, status):
    """
    Does context specific post-end actions
    :return: None
    """
    _run_function_if_in_context(
        lambda x: x.post_end_run_actions(run_id, status))


def post_log_artifact_actions(local_path, artifact_path):
    """
    Does context specific post-start actions
    :return: None
    """
    _run_function_if_in_context(
        lambda x: x.post_log_artifact_actions(
            local_path,
            artifact_path))


def post_create_experiment_actions(experiment):
    """
    Does context specific post-start actions
    :return: None
    """
    _run_function_if_in_context(
        lambda x: x.post_create_experiment_actions(experiment))
