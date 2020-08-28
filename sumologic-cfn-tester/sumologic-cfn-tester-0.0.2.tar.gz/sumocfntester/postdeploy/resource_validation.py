from postdeploy.postdeploy import PostDeploymentValidation

from common.objects import ProcessOutputs, ProcessOutput, Level


class ResourceValidator(PostDeploymentValidation):

    def __init__(self, logger, test_case, template_path, stack, assertion):
        super().__init__(logger, test_case, template_path)
        self.stack = stack
        self.assertion = assertion

    def sub_process_name(self) -> str:
        return "Resource-Validation"

    """
    Validate the resources
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        if "Resources" in self.assertion:
            # Get all Resources for Parent and Its Nested Stacks.
            all_created_resources = self._get_resource_logical_id(self.stack, None)

            assert_resources = self.assertion["Resources"]
            failed_resources = []
            if isinstance(assert_resources, list):
                for assert_resource in assert_resources:
                    if assert_resource not in all_created_resources:
                        failed_resources.append(assert_resource)
                    else:
                        all_created_resources.remove(assert_resource)
                if all_created_resources:
                    error = ProcessOutput(level=Level.WARNING,
                                          resource_name=all_created_resources,
                                          message="Extra resource created in the Stack.")
                    process_outputs.append(error)
                if failed_resources:
                    error = ProcessOutput(level=Level.ERROR,
                                          resource_name=failed_resources,
                                          message="Expected resource is not created in the Stack.")
                    process_outputs.append(error)
            else:
                if len(all_created_resources) > 0:
                    error = ProcessOutput(level=Level.WARNING,
                                          resource_name=all_created_resources,
                                          message="Extra resource created in the Stack.")
                    process_outputs.append(error)
        return process_outputs

    # Get all Nested Stack Physical Resource ID
    def _get_resource_logical_id(self, current_stack, logical_resource_id):
        all_created_resources = []
        if current_stack.resources:
            for resource in current_stack.resources:
                resource_id = logical_resource_id + "." + resource.logical_id if logical_resource_id \
                    else resource.logical_id
                all_created_resources.append(resource_id)
                nested_stack = current_stack.children.filter({"stack_id": resource.physical_id})
                if nested_stack:
                    all_created_resources.extend(self._get_resource_logical_id(nested_stack[0], resource_id))
        return all_created_resources
