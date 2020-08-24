from typing import Union, Type
import hashlib
import json

from tokko_mq_utils.core import MQPublisher

# Types
AnyException = Type[BaseException]


class ErrorSubmitter(MQPublisher):
    """Submit errors to RabbitMQ"""

    @staticmethod
    def calculate_hash(obj: Union[bytes, str, dict, list]) -> str:
        """Calculate md5 hash"""
        md5 = hashlib.md5()
        if not isinstance(obj, (str, bytes, dict, list)):
            obj = f"{obj}"
        if isinstance(obj, (dict, list)):
            obj = json.dumps(obj, sort_keys=True)
        if isinstance(obj, str):
            obj = obj.encode()
        md5.update(obj)
        return md5.hexdigest()

    def submit_error(self, error: AnyException, **extras):
        """Submit errors to RabbitMQ"""
        payload = extras.get("payload")
        reporter = extras.get("reporter", "unknown")
        payload_integrity = ""
        if payload:
            payload_integrity = self.calculate_hash(obj=payload)
        if not isinstance(reporter, str):
            reporter = f"{reporter}"
        message = json.dumps(
            {
                "exceptionRaised": type(error).__name__,
                "errorMessage": f"{error}",
                "reporter": reporter,
                "payload": payload,
                "payloadIntegrity": payload_integrity,
            }
        ).encode(encoding=extras.get("encoding", "utf8"))
        self.submit(message)
