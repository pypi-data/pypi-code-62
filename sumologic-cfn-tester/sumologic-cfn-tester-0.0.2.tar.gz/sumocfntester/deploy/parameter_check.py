import json

import cfn_flip

from common.utils import read_file
from common.objects import ProcessOutput, Level, ProcessOutputs

from deploy.deploy import Deploy


class ParameterCheck(Deploy):

    def __init__(self, logger, test_case, template_path, aws_client):
        super().__init__(logger, test_case, template_path, aws_client)
        self.parameters = self.test_data["parameters"]
        self.assertions = self.test_data["assertions"]

    def sub_process_name(self) -> str:
        return "Parameters-Check"

    """
    Run the Parameter check for the template provided and produces errors and warnings.
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        # Always convert to JSON irrespective of input as JSON or YAML.
        output_file = cfn_flip.to_json(read_file(self.template_path))
        json_data = json.loads(output_file)
        if "Parameters" in json_data:
            all_parameters = json_data["Parameters"]
            for parameter_name, parameter_value in self.parameters.items():
                if parameter_name not in all_parameters:
                    error = ProcessOutput(level=Level.ERROR, resource_name="Parameter Validation Issue",
                                          message="Provided Test Parameter -> " + parameter_name +
                                                  " is not present in the CloudFormation Template parameters.")
                    process_outputs.append(error)
        return process_outputs
