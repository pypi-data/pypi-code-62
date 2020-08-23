# Author: Jingping.zhao, 2020.6.29

from ..framework.exception import OrcSystemException, exc_grade


class FunctionBaseException(OrcSystemException):
    """
    Base function exception
    """
    code = OrcSystemException.code + exc_grade(0x3, 0x3)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Base function exception."


class BaseConfigException(FunctionBaseException):
    """
    Base config exception
    """
    code = FunctionBaseException.code + exc_grade(0x4, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Base config exception."


class BaseResourceException(FunctionBaseException):
    """
    Base resource exception
    """
    code = FunctionBaseException.code + exc_grade(0x4, 0x2)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Base resource exception."
