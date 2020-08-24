# Standard library imports

# Third party imports

# Local imports

class OnlyLowerLevelFilter():
    """Define filter to show only logs with level lower than
    """
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level
