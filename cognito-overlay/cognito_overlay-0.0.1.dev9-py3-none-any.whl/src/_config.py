import os
import boto3
import json

_client = boto3.client('secretsmanager')
_secretname = os.getenv('AUTH_SECRET_ID')

record = _client.get_secret_value(SecretId=_secretname)
config = json.loads(record['SecretString'])

CLIENT_ID = config['client_id']