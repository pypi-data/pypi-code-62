from mlflow.tracking.context.qubole_jupyter_context import QuboleJupyterContext
from mlflow.utils.qubole_pyspark_utils import QubolePySparkUtils


class QubolePySparkContext(QuboleJupyterContext):
    def _get_utils_class(self):
        return QubolePySparkUtils()
