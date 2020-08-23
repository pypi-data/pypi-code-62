# Author: Jingping.zhao, 2020.6.29

from framework.exception import OrcSystemException, exc_grade


class FunctionCloudException(OrcSystemException):
    """
    Cloud function exception
    """
    code = OrcSystemException.code + exc_grade(0x3, 0x4)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Cloud function exception."


class CloudDataException(OrcSystemException):
    """
    Cloud data exception
    """
    code = OrcSystemException.code + exc_grade(0x4, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Cloud data exception."


class CloudTemplateException(OrcSystemException):
    """
    Cloud template exception
    """
    code = OrcSystemException.code + exc_grade(0x4, 0x2)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Cloud template exception."

