import os
from .ChangeLog import ChangeLog

class CloneXls:
    def __init__(self, source_file, clone_file_postfix="_baangt"):
        """
        This class is used to make a clone of an xlsx file and than maintain a change log
        :param source_file: Path to source file
        :param clone_file_postfix: (optional) (default="_baangt") Postfix to be added in the name of clone file
        """
        self.source_file = source_file
        self.source_file_name = ".".join(source_file.split(".")[:-1])
        self.source_file_extension = source_file.split(".")[-1]
        self.clone_file = self.source_file_name + clone_file_postfix + "." + self.source_file_extension
        self.check_source_file()

    def check_source_file(self):
        if not os.path.exists(self.source_file):
            raise BaseException(f"{self.source_file} doesn't exists, please verify the path entered!")

    def update_or_make_clone(self, log_sheet_name="Change Logs", ignore_headers=[], ignore_sheets=[],
            case_sensitive_ignore=False, clone=True):
        """
        This method is used to update the clone file with the change log and if their is no clone file then make one
        :return:
        """
        if not os.path.exists(self.clone_file):
            # Will make a clone file if it doesn't exists, the cloned file will be exact copy of source
            # Change log sheets are not added here
            with open(self.source_file, "rb") as file:
                data = file.read()
            with open(self.clone_file, "wb") as file:
                file.write(data)
        elif clone:
            changeLog = ChangeLog(self.source_file, self.clone_file,
                                  log_sheet_name=log_sheet_name, ignore_headers=ignore_headers,
                                  ignore_sheets=ignore_sheets, case_sensitive_ignore=case_sensitive_ignore)
            changeLog.xlsxChangeLog()
        # Returning filename with absolute path of clone file
        return self.clone_file
