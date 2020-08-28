from process import BaseProcess

from common.objects import ProcessOutputs, ProcessOutput, Level


class PreDeploymentValidation(BaseProcess):
    """
        Aim of this file is to process the test file.
        - If test file passes schema checks, file checks
        - Go for CFN-lint and CFN-Nag validation on the CF template.
        - More classes can be added by implementing PreDeploymentValidation class.
            - Each child class should implement sub_process_name and validate function.
    """

    def __init__(self, logger, test_case, template_path, aws_client=None):
        super().__init__(logger, "Pre-Deploy-Validations")
        self.test_case = test_case
        self.test_name = test_case["TestName"]
        self.region = test_case["Region"]
        self.test_data = test_case["TestData"]
        self.template_path = template_path

    # This method should be used by child classes to provide a human readable sub process name.
    def sub_process_name(self) -> str:
        raise NotImplementedError()

    # this method should be used to implement the sub_process process. The method should return ProcessOutputs object.
    def sub_process(self) -> ProcessOutputs:
        raise NotImplementedError()

    def process(self) -> dict:
        self.logger.info("Started stage -> %s for Test Name -> %s in Region -> %s.", self.process_name, self.test_name,
                         self.region)
        errors = {}
        for sub_class in PreDeploymentValidation.__subclasses__():
            validation_errors = ProcessOutputs()
            sub_process_name = "Pre Deploy"
            try:
                class_instance = sub_class(self.logger, self.test_case, self.template_path)
                sub_process_name = class_instance.sub_process_name()
                validation_errors = class_instance.sub_process()
            except Exception as exception:
                error = ProcessOutput(level=Level.ERROR, resource_name="Pre Deploy Exception", message=str(exception))
                validation_errors.append(error)
            finally:
                if validation_errors:
                    errors[sub_process_name] = validation_errors
        self.logger.info("Completed stage -> %s for Test Name -> %s in Region -> %s.", self.process_name,
                         self.test_name,
                         self.region)
        return errors
