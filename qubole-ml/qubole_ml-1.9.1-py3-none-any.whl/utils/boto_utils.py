import boto3

from mlflow.utils.qubole_utils import \
    get_aws_keys, is_empty, is_running_in_qubole


def get_session(**kwargs):
    if is_running_in_qubole():
        access_key, secret_key = get_aws_keys()

        if not is_empty(access_key) and \
           not is_empty(secret_key):
            return boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                **kwargs
            )

    return boto3.Session(**kwargs)


def get_client(resource, **kwargs):
    return get_session().client(resource, **kwargs)
