import os
import traceback

import jsonschema

from common.utils import load_json_file, get_absolute_path, check_valid_file
from common.objects import ProcessOutput, Level, ProcessOutputs

from postdeploy.postdeploy import AssertionTypes

from process import BaseProcess


class TestFileValidator(BaseProcess):
    RESOURCE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

    def __init__(self, logger, test_file_name):
        super().__init__(logger, test_file_name)
        # Loading Schema Files
        self.test_schema = load_json_file(os.path.join(self.RESOURCE_FOLDER, "test_file.schema"))
        self.property_schema = load_json_file(os.path.join(self.RESOURCE_FOLDER, "parameter_file.schema"))
        # Get Full Path of test file
        self.test_file_full_path = os.path.realpath(test_file_name)

    """
    Read and validate the test JSON file. Validate Template and parameters JSON.
    Also, replace relative path with absolute path in the JSON object itself.
    """

    def process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        try:
            json_data = load_json_file(self.test_file_full_path)
            self.logger.debug("Reading of the file -> %s is complete.", self.test_file_full_path)
            if self.validate_json_using_schema(json_data, self.test_schema):
                success = self.validate_paths_in_test_file(json_data)
                if success:
                    if self.validate_duplicates(json_data):
                        self.logger.debug(
                            "Provided File -> %s passed all validation checks." % self.test_file_full_path)
                        return process_outputs
        except Exception as exception:
            # traceback.print_exc()
            error = ProcessOutput(level=Level.ERROR, resource_name="Test File Validation Issue", message=str(exception))
            process_outputs.append(error)
            self.logger.error(
                "Provided File -> %s failed validation checks %s." % (self.test_file_full_path, str(process_outputs)))
        return process_outputs

    def validate_json_using_schema(self, json_data, json_schema):
        self.logger.debug("Validating the file with data as %s." % str(json_data))
        try:
            jsonschema.validate(json_data, json_schema)
            self.logger.debug("Validation complete for the file.")
            return True
        except jsonschema.ValidationError as e:
            raise e

    def validate_paths_in_test_file(self, json_data):
        # Check if the template path is valid and is File.
        template_path = get_absolute_path(json_data.get("Global").get("TemplatePath"), self.test_file_full_path)
        if check_valid_file(template_path):
            self.logger.debug("Provided Template path -> %s" % template_path)
            # Check all parameters files in the test file.
            if "Tests" in json_data:
                for test in json_data.get("Tests"):
                    if "Parameters" in test:
                        parameters = test.get("Parameters")
                        if "Path" in parameters:
                            parameter_path = get_absolute_path(parameters["Path"], self.test_file_full_path)
                            if check_valid_file(parameter_path):
                                self.validate_json_using_schema(load_json_file(parameter_path), self.property_schema)
                                self.logger.debug("Provided Parameter path is %s" % parameter_path)
        return True

    @staticmethod
    def validate_duplicates(json_data):
        test_names = []
        if "Tests" in json_data:
            for test in json_data.get("Tests"):
                test_name = test["TestName"]
                assertions = test["Assertions"]
                if test_name in test_names:
                    raise Exception("Test Name - %s is duplicate in the provided Test File. "
                                    "Please make sure Test Names are unique." % test_name)
                else:
                    test_names.append(test_name)
                for assertion in assertions:
                    if not AssertionTypes.has_key(assertion["AssertType"]):
                        raise Exception("Test Name - %s has Assertion Type %s that is not valid. "
                                        "Please make sure Assertion Types is one of the following %s." %
                                        (test_name, assertion["AssertType"], AssertionTypes.all_keys()))
        return True
