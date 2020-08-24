from mlflow.tracking.context.qubole_jupyter_context import QuboleJupyterContext
from mlflow.utils.qubole_ipython_utils import QuboleIPythonUtils


class QuboleIPythonContext(QuboleJupyterContext):
    def _get_utils_class(self):
        return QuboleIPythonUtils()
