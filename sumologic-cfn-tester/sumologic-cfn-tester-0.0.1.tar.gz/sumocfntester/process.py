import json
import os
import random
import string
import sys
import time
import traceback
from abc import ABC, abstractmethod
from concurrent import futures

import cfn_flip
from common.logger import get_logger
from common.utils import check_for_error, get_instance_of_process, generate_data_each_test_case, read_file

from common.report import ReportGeneration

from common.cf_utility import Stack

from common.aws_client import AwsClient


class BaseProcess(ABC):
    def __init__(self, logger, process_name):
        self.logger = logger if logger else get_logger(__name__)
        self.process_name = process_name

    @abstractmethod
    def process(self) -> dict:
        raise NotImplementedError()

    def transform_output(self, output):
        if output:
            return {self.process_name: output}
        return None

    def get_stack(self, region, test_name):
        for stack in Stack:
            if stack.region == region and stack.test_name == test_name:
                return stack
        return None


class ProcessFlow(object):
    process_flow = ['predeploy.predeploy.PreDeploymentValidation',
                    'deploy.deploy.Deploy',
                    'postdeploy.postdeploy.PostDeploymentValidation',
                    ]

    def __init__(self, test_file, logger):
        super().__init__()
        self.test_file_name: str = test_file
        self.logger = logger if logger else get_logger(__name__)
        # Start the CloudFormation Testing Process Flow
        self.process()

    """
        Process flow iss
        1. Get the Class Instance as per the Flow. PreDeploy, Deploy, PostDeploy and CleanUp.
        2. Get the Output for each Process
        3. Generate Report for each process
        4. Append the output of each process to full output
        5. If errors in any stage, raise exception, stop process
        6. Print report and generate report.json file
    """

    def process(self):
        # First Validate the Test JSON File. If that Passes, all validation should be performed on all Test Cases.
        validator_class = get_instance_of_process("common.test_file_validator.TestFileValidator")(self.logger,
                                                                                                  self.test_file_name)
        test_file_validation_errors = validator_class.process()
        if not test_file_validation_errors:
            # Get test case for with all parameters (union of global and test case parameters).
            # Test case will be test case * regions provided in each test case
            template_path, test_data, max_workers = generate_data_each_test_case(os.path.realpath(self.test_file_name))
            all_futures = {}
            full_output = []
            aws_client = AwsClient()
            # Upload template to S3, if size exceed 51,200 bytes.
            bucket_name = self.upload_to_s3_if_required(aws_client, template_path)
            with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = {executor.submit(self.process_each_test_case, test_case, template_path, aws_client)
                           : test_case for test_case in test_data}
                all_futures.update(results)
                for future in futures.as_completed(all_futures):
                    test_case = all_futures[future]
                    test_case_validations = []
                    try:
                        test_case_validations = future.result()
                        full_output.append({"TestName": test_case["TestName"], "Region": test_case["Region"],
                                            "Validations": test_case_validations})
                    except Exception as exc:
                        # traceback.print_exc()
                        self.logger.error("Test Case -> %s failed with validation as %s", test_case["TestName"],
                                          test_case_validations)
            # Generate Report for Console and Report File.
            ReportGeneration.generate_report(full_output, self.test_file_name, template_path, self.logger)
            # Clean Up for S3 Bucket
            aws_client.delete_bucket(bucket_name)
        else:
            self.logger.error("Validation Failed for Test File with Errors as : \n %s" % (
                json.dumps(test_file_validation_errors, indent=4, default=ReportGeneration.object_to_dictionary)))

    def process_each_test_case(self, test_case, template_path, aws_client):
        test_case_validations = []
        try:
            for process in self.process_flow:
                process_name, process_errors = self.run_process(process, test_case, template_path, aws_client)
                if process_errors:
                    test_case_validations.append(process_errors)
                    if check_for_error(process_name, process_errors):
                        break
        finally:
            process_name, process_errors = self.run_process('cleanup.cleanup.CleanUp', test_case, template_path,
                                                            aws_client)
            if process_errors:
                test_case_validations.append(process_errors)

        return test_case_validations

    def run_process(self, process, test_case, template_path, aws_client):
        process_instance = get_instance_of_process(process)(self.logger, test_case, template_path, aws_client)
        output = process_instance.transform_output(process_instance.process())
        if output:
            return process_instance.process_name, output
        return None, None

    def upload_to_s3_if_required(self, aws_client, template_path):
        output_file = cfn_flip.to_json(read_file(template_path))
        size = sys.getsizeof(output_file)
        if size > 51200:
            self.logger.info("Size of the Template -> %s which is greater than max limit of 51,200 bytes.", size)
            bucket_name = string.ascii_lowercase
            bucket_name = ''.join(random.choice(bucket_name) for i in range(10))
            bucket_name = "sumo-tf-" + bucket_name
            s3_client = aws_client.s3_client_instance("us-east-1")
            aws_client.create_bucket(s3_client, bucket_name)
            time.sleep(30)
            file_url = aws_client.upload_to_bucket(s3_client, bucket_name, template_path)
            self.logger.info("Uploaded template to S3 with URL as %s", file_url)
            return bucket_name
        return None
