import traceback

from common.objects import ProcessOutput, Level, ProcessOutputs

from cleanup.cleanup import CleanUp


class DeleteStack(CleanUp):

    def __init__(self, logger, test_case, template_path, stack):
        super().__init__(logger, test_case, template_path)
        self.parameters = self.test_data["parameters"]
        self.assertions = self.test_data["assertions"]
        self.stack = stack

    def sub_process_name(self) -> str:
        return "Delete-Stack"

    """
    Delete Stacks provided and produces errors and warnings.
    """

    def sub_process(self) -> ProcessOutputs:
        process_outputs = ProcessOutputs()
        try:
            self.stack.delete_stack()
        except Exception as e:
            # traceback.print_exc()
            error = ProcessOutput(level=Level.ERROR, message=str(e), stack_name=self.stack.stack_name)
            process_outputs.append(error)
        self.logger.debug("Delete Stack complete with errors as %s", process_outputs)
        return process_outputs
