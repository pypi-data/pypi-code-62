import copy 

class StatusCodeCopy:

    @staticmethod
    def copy(status_code_obj, message):
        status_code = copy.deepcopy(status_code_obj)
        status_code.update_msg(message)
        return status_code