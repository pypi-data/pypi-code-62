from postdeploy.postdeploy import PostDeploymentValidation

from common.objects import ProcessOutputs, ProcessOutput, Level


class OutputValidator(PostDeploymentValidation):

    def __init__(self, logger, test_case, template_path, stack, assertion):
        super().__init__(logger, test_case, template_path)
        self.stack = stack
        self.assertion = assertion

    def sub_process_name(self) -> str:
        return "Output-Validation"

    """
        Validate the outputs
        """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        if "Outputs" in self.assertion:
            # Get all Resources for Parent and Its Nested Stacks.
            all_created_outputs = self._get_output_keys(self.stack, None)

            assert_outputs = self.assertion["Outputs"]
            if isinstance(assert_outputs, list):
                failed_outputs = []
                for assert_output in assert_outputs:
                    if assert_output not in all_created_outputs:
                        failed_outputs.append(assert_output)
                    else:
                        all_created_outputs.remove(assert_output)
                if all_created_outputs:
                    error = ProcessOutput(level=Level.WARNING,
                                          resource_name=all_created_outputs,
                                          message="Extra Outputs created in the Stack.")
                    process_outputs.append(error)
                if failed_outputs:
                    error = ProcessOutput(level=Level.ERROR,
                                          resource_name=failed_outputs,
                                          message="Expected output is not created in the Stack.")
                    process_outputs.append(error)
            else:
                if len(all_created_outputs) > 0:
                    error = ProcessOutput(level=Level.WARNING,
                                          resource_name=all_created_outputs,
                                          message="Extra resource created in the Stack.")
                    process_outputs.append(error)
        return process_outputs

    # Get all Nested Stack Physical Resource ID
    def _get_output_keys(self, current_stack, logical_resource_id):
        all_created_outputs = []
        if current_stack.outputs:
            for output in current_stack.outputs:
                output_key = logical_resource_id + "." + output.key if logical_resource_id else output.key
                all_created_outputs.append(output_key)

        for child in current_stack.children:
            child_resource = current_stack.resources.filter({"physical_id": child.stack_id})
            key = logical_resource_id + "." + child_resource[0].logical_id if logical_resource_id \
                else child_resource[0].logical_id
            all_created_outputs.extend(self._get_output_keys(child, key))
        return all_created_outputs
