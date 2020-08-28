from common.objects import ProcessOutput, Level, ProcessOutputs

from deploy.deploy import Deploy

from common.cf_utility import Stack


class DeployStack(Deploy):

    def __init__(self, logger, test_case, template_path, aws_client):
        super().__init__(logger, test_case, template_path, aws_client)
        self.parameters = self.test_data["parameters"]
        self.assertions = self.test_data["assertions"]
        self.stack = Stack(test_name=self.test_name, region=self.region, test_data=self.test_data,
                           template_path=template_path, logger=logger, aws_client=aws_client)

    def sub_process_name(self) -> str:
        return "Deploy-Stack"

    """
    Deploy template provided and produces errors and warnings.
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        status, errors = self.stack.deploy_template()
        if status != "PASS":
            for error in errors:
                error = ProcessOutput(level=Level.ERROR, resource_name=error["Resources"],
                                      message=error["Message"],
                                      stack_name=self.stack.stack_name)
                process_outputs.append(error)
        self.logger.debug("Deploy Stack complete with errors as %s", process_outputs)
        return process_outputs
