import json

from predeploy.predeploy import PreDeploymentValidation
from common.utils import run_command
from common.objects import ProcessOutput, Level, ProcessOutputs


class CfnLint(PreDeploymentValidation):

    def __init__(self, logger, test_case, template_path):
        super().__init__(logger, test_case, template_path)

    def sub_process_name(self) -> str:
        return "Cfn-Lint"

    """
    Run the cfn linting for the template provided and produces errors and warnings.
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        try:
            commands = ["cfn-lint", "-t", self.template_path, "-f", "json"]
            if self.logger.level == "DEBUG":
                commands.extend(["-D", "True"])
            elif self.logger.level == "INFO":
                commands.extend(["-I", "True"])
            self.logger.debug("Running command for CFN Lint as %s", ' '.join(commands))

            response = run_command(commands)
            self.logger.debug(
                "CFN Lint for the template %s is complete with result as %s." % (self.template_path, response))

            self.transform_process_output_data(json.loads(response), process_outputs)
        except Exception as exception:
            error = ProcessOutput(level=Level.ERROR, resource_name="CFN Lint Exception", message=str(exception))
            process_outputs.append(error)
            self.logger.error(
                "Test Case -> %s, CFN Lint Failed with %s." % (self.test_name, str(process_outputs)))
        return process_outputs

    def transform_process_output_data(self, issues, process_outputs):
        if issues:
            for issue in issues:
                error = ProcessOutput(level=Level.WARNING if "Warning" in issue["Level"] else Level.ERROR,
                                      line_number=issue["Location"]["Start"], resource_name="CFN Lint Validation Issue",
                                      message=issue["Rule"]["Id"] + " - " + issue["Message"])
                process_outputs.append(error)
