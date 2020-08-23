import boto3
from botocore.exceptions import ClientError

class crossAccountSecrets(object):
    def __init__(self, sourceAccountProfile, sourceSecretsRegion, sourceSecretsEnvFilter, destinationAccountProfile, destinationSecretsRegion, destinationAccountKMS):
        # source session
        sourceSession = boto3.session.Session(profile_name = sourceAccountProfile)
        self.srcClient = sourceSession.client(service_name = "secretsmanager", region_name  = sourceSecretsRegion)
        self.srcSecretsEnvFilter = sourceSecretsEnvFilter

        # destination session
        destinationSession = boto3.session.Session(profile_name = destinationAccountProfile)
        self.dstClient = destinationSession.client(service_name = "secretsmanager", region_name  = destinationSecretsRegion)
        self.dstClientKMS = destinationAccountKMS

    def replicate(self):
        try:
            # retrieve all secrts matching given filter
            paginator = self.srcClient.get_paginator("list_secrets").paginate()
            for page in paginator:
                for secret in page["SecretList"]:
                    if self.srcSecretsEnvFilter in secret["Name"]:
                        value = self.srcClient.get_secret_value(SecretId=secret["Name"])
                        self.__putSecret((secret["Name"]), value["SecretString"])
        except ClientError as e:
            raise e

    def __putSecret(self, key, value):
        print(f"# Replicating secret: {key}\n")
        try:
            # create new secret with key and value
            self.dstClient.create_secret(Name = key, SecretString = value, KmsKeyId = self.dstClientKMS)
        except ClientError as e:
            # update existing secret with key as key and new value as value
            if e.response["Error"]["Code"] == "ResourceExistsException": # update existing secret
                self.dstClient.update_secret(SecretId = key, SecretString = value, KmsKeyId = self.dstClientKMS)
            else:
                raise e

def sync(sourceAccountProfile, sourceSecretsRegion, sourceSecretsEnvFilter, destinationAccountProfile, destinationSecretsRegion, destinationAccountKMS):
    return crossAccountSecrets(sourceAccountProfile, sourceSecretsRegion, sourceSecretsEnvFilter, destinationAccountProfile, destinationSecretsRegion, destinationAccountKMS).replicate()
