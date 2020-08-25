from io import BytesIO

from azure.storage.blob import BlobClient


def create_blob_client_stream(url, credential):
    stream = None

    try:
        blob_client = BlobClient.from_blob_url(blob_url=url, credential=credential)
        stream_downloader = blob_client.download_blob()
        stream = BytesIO()
        stream_downloader.readinto(stream)
    except ConnectionError as e:
        raise Exception(e)

    finally:
        return stream


class BlobAPI:
    def __init__(self, layer):
        self.layer = layer

        self.create_blob_client_stream = create_blob_client_stream
