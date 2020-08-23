# Author: Jingping.zhao


def exc_grade(grade, index):
    return pow(0x10, (0x8 - grade)) * index


class OrcException(Exception):
    """
    Envision
    """
    code = 0x00000000

    def __init__(self, info=None):
        self.info = info or "Basic exception."

    def __str__(self):
        return "<0x%X, %s>" % (self.code, self.info)


class OrcSystemException(OrcException):
    """
    System Exception 01
    """
    code = OrcException.code + exc_grade(0x2, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "System exception."


class OrcUtilException(OrcException):
    """
    Standard Util Exception
    """
    code = OrcException.code + exc_grade(0x2, 0x2)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Standard util exception."


class OrcLibraryException(OrcSystemException):
    """
    Library Exception
    """
    code = OrcSystemException.code + exc_grade(0x3, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework exception."


class OrcFrameworkException(OrcSystemException):
    """
    Framework Exception
    """
    code = OrcSystemException.code + exc_grade(0x3, 0x2)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework exception."


class OrcLibraryCommonException(OrcLibraryException):
    """
    Framework Exception
    """
    code = OrcLibraryException.code + exc_grade(0x4, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework exception."


class OrcFrameworkLibException(OrcFrameworkException):
    """
    Framework Lib Exception
    """
    code = OrcFrameworkException.code + exc_grade(0x4, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework lib exception."


class OrcFrameworkLibStringException(OrcFrameworkLibException):
    """
    Framework Lib Exception
    """
    code = OrcFrameworkLibException.code + exc_grade(0x5, 0x1)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework lib string exception."


class OrcFrameworkProcessException(OrcFrameworkException):
    """
    Framework Layer Exception
    """
    code = OrcFrameworkException.code + exc_grade(0x4, 0x2)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework layer exception."


class OrcFrameworkDatabaseException(OrcFrameworkException):
    """
    Framework Database Exception
    """
    code = OrcFrameworkException.code + exc_grade(0x4, 0x3)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework database exception."


class OrcFrameworkApiException(OrcFrameworkException):
    """
    Framework Api Exception
    """
    code = OrcFrameworkException.code + exc_grade(0x4, 0x4)

    def __init__(self, code, info=None):
        self.code += code
        self.info = info or "Framework api exception."
