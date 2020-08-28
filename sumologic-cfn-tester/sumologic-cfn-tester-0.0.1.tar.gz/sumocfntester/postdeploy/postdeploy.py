import traceback
from enum import Enum, unique

from common.objects import ProcessOutput, Level, ProcessOutputs
from process import BaseProcess
from common.utils import get_instance_of_process


@unique
class AssertionTypes(Enum):
    ResourceExistence = "postdeploy.resource_validation.ResourceValidator"
    OutputsCheck = "postdeploy.output_validation.OutputValidator"
    ParameterCheck = "postdeploy.parameter_check.ParameterCheck"

    @classmethod
    def has_key(cls, name):
        return any(x for x in cls if x.name == name)

    @classmethod
    def all_keys(cls):
        return ", ".join(c.name for c in sorted(AssertionTypes))


class PostDeploymentValidation(BaseProcess):

    def __init__(self, logger, test_case, template_path, aws_client=None):
        super().__init__(logger, "Post-Deploy-Validations")
        self.test_case = test_case
        self.test_name = test_case["TestName"]
        self.region = test_case["Region"]
        self.test_data = test_case["TestData"]
        self.template_path = template_path
        self.parameters = self.test_data["parameters"]
        self.assertions = self.test_data["assertions"]

    # This method should be used by child classes to provide a human readable sub process name.
    def sub_process_name(self) -> str:
        raise NotImplementedError()

    # this method should be used to implement the sub_process process. The method should return ProcessOutputs object.
    def sub_process(self) -> ProcessOutputs:
        raise NotImplementedError()

    def process(self) -> dict:
        self.logger.info("Started stage -> %s for Test Name -> %s in Region -> %s.", self.process_name,
                         self.test_name, self.region)
        errors = {}
        current_stack = self.get_stack(self.region, self.test_name)
        if current_stack:
            for assertion in self.assertions:
                validation_errors = ProcessOutputs()
                sub_process_name = "Post Deploy"
                try:
                    class_instance = get_instance_of_process(
                        AssertionTypes[assertion["AssertType"]].value)(self.logger, self.test_case, self.template_path,
                                                                       current_stack, assertion["Assert"])
                    sub_process_name = class_instance.sub_process_name()
                    validation_errors = class_instance.sub_process()
                except Exception as exception:
                    # traceback.print_exc()
                    error = ProcessOutput(level=Level.ERROR, resource_name="Post Deploy Exception",
                                          message=str(exception))
                    validation_errors.append(error)
                finally:
                    if validation_errors:
                        errors[sub_process_name] = validation_errors
        else:
            self.logger.info("No Stack Found with Test Name -> %s and Region -> %s.", self.test_name, self.region)
        self.logger.info("Completed stage -> %s for Test Name -> %s in Region -> %s.", self.process_name,
                         self.test_name, self.region)
        return errors
