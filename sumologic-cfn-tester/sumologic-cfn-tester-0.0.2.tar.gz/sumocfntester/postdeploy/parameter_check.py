from postdeploy.postdeploy import PostDeploymentValidation

from common.objects import ProcessOutputs, ProcessOutput, Level


class ParameterCheck(PostDeploymentValidation):

    def __init__(self, logger, test_case, template_path, stack, assertion):
        super().__init__(logger, test_case, template_path)
        self.stack = stack
        self.assertion = assertion

    def sub_process_name(self) -> str:
        return "Parameter-Check"

    """
        Validate the Parameters passed to Nested Stacks
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        # Get all Resources for Parent and Its Nested Stacks.
        all_parameters = self._get_all_parameters(self.stack, None)

        for resource_name, parameters in self.assertion.items():
            created_parameters = all_parameters.get(resource_name, None)
            failed_parameter = {}
            if created_parameters:
                for parameter_name, parameter_value in parameters.items():
                    created_value = self._get_created_value(parameter_name, created_parameters)
                    if parameter_value not in created_value:
                        failed_parameter[parameter_name] = "Parameter check failed with Expected Value -> " \
                                                           + parameter_value + \
                                                           " and Created Value -> " + created_value
            else:
                error = ProcessOutput(level=Level.ERROR,
                                      resource_name=resource_name,
                                      message="Expected resource is not created in the Stack.")
                process_outputs.append(error)
            if failed_parameter:
                error = ProcessOutput(level=Level.ERROR,
                                      resource_name=resource_name,
                                      message=failed_parameter)
                process_outputs.append(error)
        return process_outputs

    @staticmethod
    def _get_created_value(parameter_name, created_parameters):
        for value in created_parameters:
            if parameter_name == value["ParameterKey"]:
                return value["ParameterValue"]

    # Get all Nested Stack Physical Resource ID
    def _get_all_parameters(self, current_stack, logical_resource_id):
        all_parameters = {}
        if current_stack:
            for child in current_stack.children:
                child_resource = current_stack.resources.filter({"physical_id": child.stack_id})
                key = logical_resource_id + "." + child_resource[0].logical_id if logical_resource_id \
                    else child_resource[0].logical_id
                all_parameters[key] = child.created_parameters
                all_parameters.update(self._get_all_parameters(child, key))
        return all_parameters
