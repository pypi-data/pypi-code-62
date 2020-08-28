import os
import threading

import boto3
import cfn_flip
from boto3.s3.transfer import S3Transfer

from common.utils import read_file


class AwsClient(object):

    def __init__(self):
        self.client_lock = threading.RLock()

    __cf_clients = {}
    file_url = None

    def cf_client_instance(self, region):
        with self.client_lock:
            if not self.__cf_clients.get(region):
                self.__cf_clients[region] = boto3.client("cloudformation", region)
        return self.__cf_clients.get(region)

    def s3_client_instance(self, region):
        with self.client_lock:
            s3_client = boto3.client("s3", region)
        return s3_client

    def describe_stacks(self, cf_client, stack_identifier):
        stack_details = None
        with self.client_lock:
            if stack_identifier:
                stack_details = cf_client.describe_stacks(StackName=stack_identifier)["Stacks"][0]
        return stack_details

    def create_stack(self, cf_client, stack_name, template_path, parameters, capability):
        response = None
        with self.client_lock:
            if stack_name:
                if self.file_url:
                    response = cf_client.create_stack(StackName=stack_name, TemplateURL=self.file_url,
                                                      Parameters=parameters, Capabilities=capability)
                else:
                    output_file = cfn_flip.to_json(read_file(template_path))
                    response = cf_client.create_stack(StackName=stack_name, TemplateBody=output_file,
                                                      Parameters=parameters, Capabilities=capability)
        return response

    def delete_stack(self, cf_client, stack_identifier, failed_resources_ids=None):
        response = None
        with self.client_lock:
            if stack_identifier:
                if failed_resources_ids:
                    cf_client.delete_stack(StackName=stack_identifier, RetainResources=failed_resources_ids)
                else:
                    cf_client.delete_stack(StackName=stack_identifier)
        return response

    def list_stack_resources(self, cf_client, stack_identifier):
        response = []
        with self.client_lock:
            if stack_identifier:
                for page in cf_client.get_paginator("list_stack_resources").paginate(StackName=stack_identifier):
                    response.extend(page["StackResourceSummaries"])
        return response

    def list_stack_events(self, cf_client, stack_identifier):
        response = []
        with self.client_lock:
            if stack_identifier:
                for page in cf_client.get_paginator("describe_stack_events").paginate(StackName=stack_identifier):
                    response.extend(page["StackEvents"])
        return response

    def create_bucket(self, s3_client, bucket_name):
        with self.client_lock:
            response = s3_client.create_bucket(Bucket=bucket_name)
        return response['Location']

    def upload_to_bucket(self, s3_client, bucket_name, template_path):
        with self.client_lock:
            transfer = S3Transfer(s3_client)
            head, tail = os.path.split(template_path)
            transfer.upload_file(template_path, bucket_name, tail, extra_args={'ACL': 'public-read'})
            self.file_url = '%s/%s/%s' % (s3_client.meta.endpoint_url, bucket_name, tail)
        return self.file_url

    def delete_bucket(self, bucket_name):
        if bucket_name:
            with self.client_lock:
                bucket = boto3.resource('s3').Bucket(bucket_name)
                bucket.objects.all().delete()
                bucket.delete()
