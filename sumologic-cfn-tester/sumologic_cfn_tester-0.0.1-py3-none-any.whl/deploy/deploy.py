from common.objects import ProcessOutput, Level, ProcessOutputs
from process import BaseProcess
from common.utils import get_instance_of_process


class Deploy(BaseProcess):
    """
        - Create the parameters to deploy the template
        - Deploy the template along with parameters using deploy with s3 bucket.
    """

    def __init__(self, logger, test_case, template_path, aws_client):
        super().__init__(logger, "Deploy")
        self.test_case = test_case
        self.test_name = test_case["TestName"]
        self.region = test_case["Region"]
        self.test_data = test_case["TestData"]
        self.template_path = template_path
        self.aws_client = aws_client

    # This method should be used by child classes to provide a human readable sub process name.
    def sub_process_name(self) -> str:
        raise NotImplementedError()

    # this method should be used to implement the sub_process process. The method should return ProcessOutputs object.
    def sub_process(self) -> ProcessOutputs:
        raise NotImplementedError()

    process_flow = ['deploy.parameter_check.ParameterCheck', 'deploy.stack_deploy.DeployStack']

    def process(self) -> dict:
        self.logger.info("Started stage -> %s for Test Name -> %s in Region -> %s.", self.process_name,
                         self.test_name, self.region)
        errors = {}
        # First validate the parameters are provided correctly for each test case
        # Then deploy each test case in regions provided using threading.
        for sub_process in self.process_flow:
            validation_errors = ProcessOutputs()
            sub_process_name = "Deploy"
            try:
                class_instance = get_instance_of_process(sub_process)(self.logger, self.test_case, self.template_path,
                                                                      self.aws_client)
                sub_process_name = class_instance.sub_process_name()
                validation_errors = class_instance.sub_process()
            except Exception as exception:
                error = ProcessOutput(level=Level.ERROR, resource_name="Deploy Exception", message=str(exception))
                validation_errors.append(error)
            finally:
                if validation_errors:
                    errors[sub_process_name] = validation_errors
                    break
        self.logger.info("Completed stage -> %s for Test Name -> %s in Region -> %s.", self.process_name,
                         self.test_name, self.region)
        return errors
