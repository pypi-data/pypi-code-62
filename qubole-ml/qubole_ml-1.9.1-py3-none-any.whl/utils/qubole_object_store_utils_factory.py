from mlflow.utils.qubole_s3_utils import QuboleS3Utils
from mlflow.utils.qubole_gcs_utils import QuboleGCSUtils


class QuboleObjectStoreUtilsFactory(object):
    @classmethod
    def get_utils(cls, uri_scheme):
        provider_classes = [QuboleS3Utils, QuboleGCSUtils]
        return next(
            filter(
                lambda x: x.in_context(uri_scheme),
                map(
                    lambda x: x(),
                    provider_classes
                )),
            QuboleS3Utils()
        )
