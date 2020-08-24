from mlflow.utils.qubole_ipython_utils import QuboleIPythonUtils
from mlflow.utils.qubole_pyspark_utils import QubolePySparkUtils


class QuboleContextUtilsFactory(object):
    @classmethod
    def get_utils(cls):
        provider_classes = [QuboleIPythonUtils, QubolePySparkUtils]
        return next(
            filter(
                lambda x: x.in_context(),
                map(
                    lambda x: x(),
                    provider_classes
                )),
            QubolePySparkUtils()
        )
