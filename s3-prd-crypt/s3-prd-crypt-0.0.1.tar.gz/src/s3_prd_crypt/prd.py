# -*- coding: utf-8 -*-
from io import BytesIO
import pandas as pd

from s3_connector import AWSS3Connector


def s3_put_object(
        s3_access_key: str,
        s3_access_secret_key: str,
        bucket_name: str,
        obj_path: str,
        df: pd.DataFrame,
        endpoint: str = None,
        encrypt: bool = False,
        key: bytes = None):

    """Put DataFrame in AWS S3. DataFrame is stored as parquet file with pandas.DataFrame.to_parquet() with default
    parameters and pyarrow engine.

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:              str, path to store data
    :param df:                    pd.DataFrame, data to put in S3
    :param endpoint:              str, optional,  endpoint, should, if given, be a https endpoint to ensure that the key
                                  and data are  sent securely before encryption and storage, default = None

    :param encrypt:               bool, optional, whether data should be encrypted, default=False

                                  Data are encrypted with the encryption algorithm AES-256 and AWS SSE-C, server-side
                                  encryption with customer-provided encryption keys. This means that the data are
                                  encrypted before storage with a key provided by the user (you).
                                  The user is responsible for not losing the key as it is needed for decrypting the data.
                                  (https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)

    :param key:                   bytes, key to encrypt with if encrypt = True, default = None
    """

    s3_connector = AWSS3Connector(access_key=s3_access_key,
                                  secret_key=s3_access_secret_key,
                                  bucket_name=bucket_name,
                                  host=endpoint)

    pq_buffer = BytesIO()
    df.to_parquet(pq_buffer)
    data = pq_buffer.getvalue()

    if encrypt:
        s3_connector.put_encrypt_sse_c(data=data,
                                       obj_name=obj_path,
                                       key=key)
    else:
        s3_connector.put(data=data,
                         obj_name=obj_path)


def s3_read_object(
        s3_access_key: str,
        s3_access_secret_key: str,
        bucket_name: str,
        obj_path: str,
        endpoint: str = None,
        encrypted: bool = False,
        key: bytes = None) -> pd.DataFrame:

    """Read DataFrame stored as parquet with pandas.DataFrame.to_parquet() default parameters and pyarrow engine.

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:             str, path to read data from
    :param endpoint:              str, endpoint, should, if given, be a https endpoint to ensure that the key and data
                                  are sent securely before encryption and storage, default = None

    :param encrypted:             bool, optional, whether data should be decrypted, default=False

                                  If data are encrypted, data must be encrypted with the encryption algorithm AES-256
                                  and AWS SSE-C, server-side encryption with customer-provided encryption keys. The key
                                  that was used for encryption is needed for decrypting the data.
                                  (https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)

    :param key:                   bytes, key to encrypt with if encrypt = True, default = None

    :return data:                 pd.DataFrame, data read from S3"""

    s3_connector = AWSS3Connector(access_key=s3_access_key,
                                  secret_key=s3_access_secret_key,
                                  bucket_name=bucket_name,
                                  host=endpoint)

    if encrypted:
        res = s3_connector.read_decrypt_sse_c(obj_name=obj_path,
                                              key=key)
    else:
        res = s3_connector.read(obj_name=obj_path)

    return pd.read_parquet(BytesIO(res))


def s3_delete_object(s3_access_key: str,
                     s3_access_secret_key: str,
                     bucket_name: str,
                     obj_path: str,
                     endpoint: str = None):

    """Delete stored object in S3

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:              str, path of object to delete
    :param endpoint:              str, endpoint, should, if given, be a https endpoint to ensure that the key and data
                                  are sent securely before encryption and storage, default = None
    """

    s3_connector = AWSS3Connector(access_key=s3_access_key,
                                  secret_key=s3_access_secret_key,
                                  bucket_name=bucket_name,
                                  host=endpoint)

    s3_connector.delete(obj_name=obj_path)