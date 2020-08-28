import json

from predeploy.predeploy import PreDeploymentValidation
from common.utils import run_command
from common.objects import ProcessOutput, Level, ProcessOutputs


class CfnNag(PreDeploymentValidation):

    def __init__(self, logger, test_case, template_path):
        super().__init__(logger, test_case, template_path)

    def sub_process_name(self) -> str:
        return "Cfn-Nag"

    """
    Run the cfn Nag for the template provided and produces errors and warnings.
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        try:
            commands = ["cfn_nag", self.template_path, "-u", "json"]
            if self.logger.level == "DEBUG":
                commands.extend(["-d", "True"])
            self.logger.debug("Running command for CFN Nag as %s", ' '.join(commands))

            response = run_command(commands)
            self.logger.debug(
                "CFN Nag for the template %s is complete with result as %s." % (self.template_path, response))

            self.transform_process_output_data(json.loads(response), process_outputs)
        except Exception as exception:
            error = ProcessOutput(level=Level.ERROR, resource_name="CFN Nag Exception", message=str(exception))
            process_outputs.append(error)
            self.logger.error(
                "Test Case -> %s, CFN Nag Failed with %s." % (self.test_name, str(process_outputs)))
        return process_outputs

    @staticmethod
    def transform_process_output_data(issues, process_outputs):
        if issues:
            for issue in issues:
                for validation in issue["file_results"]["violations"]:
                    error = ProcessOutput(level=Level.WARNING if "WARN" in validation["type"] else Level.ERROR,
                                          line_number=CfnNag.transform_line_numbers(validation["line_numbers"]),
                                          resource_name=validation["logical_resource_ids"],
                                          message=validation["id"] + " - " + validation["message"])
                    process_outputs.append(error)

    @staticmethod
    def transform_line_numbers(line_numbers):
        output = []
        for line_number in line_numbers:
            output.append({'LineNumber': line_number})
        return output
