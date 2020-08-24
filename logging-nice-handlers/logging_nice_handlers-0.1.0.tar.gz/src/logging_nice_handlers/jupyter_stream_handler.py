# Standard library imports
import os
import sys
import logging
from logging import Handler

# Third party imports
from char import char

# Local imports
from .filters import OnlyLowerLevelFilter

STR_STDOUT_FORMAT = "%(message)s"
STR_STDERR_FORMAT = "[%(levelname)s]: %(message)s"

class JupyterStreamHandler(Handler):
    """Logger handler which shows important messages in red
    """

    @char
    def __init__(
            self,
            int_min_stdout_level=logging.INFO,
            int_min_stderr_level=logging.WARNING,
    ):
        """Initialize base handler and list of 2 handlers

        Args:
            int_min_stdout_level (int, optional): min level to just show.
            int_min_stderr_level (int, optional): min level to show in red.
        """

        Handler.__init__(self)
        self.list_handlers = []
        #####
        # 1) Add stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(level=int_min_stdout_level)
        stdout_handler.setFormatter(logging.Formatter(STR_STDOUT_FORMAT))
        stdout_handler.addFilter(OnlyLowerLevelFilter(int_min_stderr_level))
        self.list_handlers.append(stdout_handler)
        #####
        # 2) Add stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(level=int_min_stderr_level)
        stderr_handler.setFormatter(logging.Formatter(STR_STDERR_FORMAT))
        self.list_handlers.append(stderr_handler)


    def emit(self, record):
        """function that handles sent messages

        Args:
            record (logging.record): message that given to logger
        """
        for handler in self.list_handlers:
            if record.levelno >= handler.level:
                handler.emit(record)

