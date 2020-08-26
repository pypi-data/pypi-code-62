from typing import Tuple
from uuid import uuid4


class MultipartEncoder:
    def __init__(self, fields=None, files=None):
        # name, value
        self.fields: List[bytes, bytes] = fields or []

        # field_name, file_name, content_type, body
        self.files: List[bytes, bytes, bytes, bytes] = files or []

    def encode(self) -> Tuple[str, bytes]:
        boundary = uuid4().hex
        _boundary = f"--{boundary}".encode()
        data = b""

        if self.fields:
            data += b"".join(
                b"%s\r\n"
                b'Content-Disposition: form-data; name="%s"\r\n'
                b"\r\n"
                b"%s\r\n\r\n" % (_boundary, name, value)
                for name, value in self.fields
            )

        if self.files:
            data += b"".join(
                b"%s\r\n"
                b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                b"Content-Type: %s\r\n"
                b"\r\n"
                b"%s\r\n\r\n" % (_boundary, field_name, file_name, content_type, body)
                for field_name, file_name, content_type, body in self.files
            )

        data += b"%s--\r\n\r\n" % _boundary

        return f"multipart/form-data; boundary={boundary}", data
