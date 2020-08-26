# -*- coding: utf-8 -*-

"""
Define user's exception
"""


class OpenMdfError(Exception):
    """
    use mdfreader to open mf4-file error
    """

    def __init__(self):
        pass

    def __str__(self):
        return "Use the third-module mdfreader to open MF4 file error"


class OpenDbError(Exception):
    """
    use mdfreader to open mf4-file error
    """

    def __init__(self, fun=None):
        self.fun = fun

    def __str__(self):
        return f"open the db Error in fun:{self.fun}"
