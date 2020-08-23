# Standard library imports
import os
import logging
from logging import Handler
from collections import OrderedDict

# Third party imports
from char import char

# Local imports

# Define Constants
STR_MSG_FILE_FORMAT = '%(asctime)s - [%(levelname)s]: %(message)s'
STR_FILE_LOG_FORMAT = logging.Formatter(
    STR_MSG_FILE_FORMAT, "%Y-%m-%d %H:%M:%S")


DICT_FILENAME_BY_LOG_LEVEL = OrderedDict()
DICT_FILENAME_BY_LOG_LEVEL[10] = "10_debug_msgs.log"
DICT_FILENAME_BY_LOG_LEVEL[20] = "20_info_msgs.log"
DICT_FILENAME_BY_LOG_LEVEL[30] = "30_warning_msgs.log"
DICT_FILENAME_BY_LOG_LEVEL[40] = "40_error_msgs.log"


class AllLevelFileHandler(Handler):
    """Logger handler which saves messages for all set levels in one folder
    """

    @char
    def __init__(
            self,
            str_path_dir_with_logs="Logs",
            str_open_mode="w",
    ):
        """Initialize base handler and list of file handlers for all levels

        Args:
            str_path_dir_with_logs (str, optional): where to save logs for all levels.
            str_open_mode (str, optional): open mode for a new logger
        """
        Handler.__init__(self)
        # Create folder for Logs if it is necessary
        if not os.path.isdir(str_path_dir_with_logs):
            os.makedirs(str_path_dir_with_logs)
        #####
        self.list_all_level_handlers = []
        for int_level in DICT_FILENAME_BY_LOG_LEVEL:
            str_log_filename = DICT_FILENAME_BY_LOG_LEVEL[int_level]
            current_handler = logging.FileHandler(
                os.path.join(str_path_dir_with_logs, str_log_filename),
                mode=str_open_mode,
            )
            current_handler.setLevel(level=int_level)
            # Add format
            current_handler.setFormatter(STR_FILE_LOG_FORMAT)
            self.list_all_level_handlers.append(current_handler)

    def emit(self, record):
        """function that handles sent messages

        Args:
            record (logging.record): message that given to logger
        """
        for current_file_handler in self.list_all_level_handlers:
            if record.levelno >= current_file_handler.level:
                current_file_handler.emit(record)


