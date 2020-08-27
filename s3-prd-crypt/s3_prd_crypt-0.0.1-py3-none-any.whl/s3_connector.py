# -*- coding: utf-8 -*-
import boto3


class AWSS3Connector:
    """Amazon S3 Storage compatible connection"""

    def __init__(self, access_key, secret_key, host, bucket_name):

        self.s3 = boto3.resource(
            service_name='s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            #verify=os.getenv('CERT_PATH'),
            endpoint_url=host
        )

        if bucket_name not in [bucket.name for bucket in self.s3.buckets.all()]:
            raise ValueError(f"{bucket_name} does not exist.")

        self.bucket = self.s3.Bucket(bucket_name)

    def put(self, data: bytes, obj_name: str):
        obj = self.s3.Object(self.bucket.name, obj_name)
        obj.put(Body=data)

    def put_encrypt_sse_c(self, data: bytes, obj_name: str, key: bytes):
        """Writing and encrypting data with server side encryption and customer-provided encryption key"""
        obj = self.s3.Object(self.bucket.name,
                             obj_name)
        obj.put(Body=data,
                SSECustomerKey=key,
                SSECustomerAlgorithm="AES256")

    def read(self, obj_name: str) -> bytes:
        obj = self.s3.Object(self.bucket.name, obj_name)
        return obj.get()['Body'].read()

    def read_decrypt_sse_c(self, obj_name: str, key: bytes) -> bytes:
        """Reading and decrypting data with server side encryption and customer-provided encryption key"""
        obj = self.s3.Object(self.bucket.name, obj_name)
        return obj.get(SSECustomerKey=key,
                       SSECustomerAlgorithm="AES256")['Body'].read()

    def delete(self, obj_name):
        obj = self.s3.Object(self.bucket.name, obj_name)
        obj.delete()
