"""
Defines the abstract base class for other validators to inherit from.
"""

class AbstractValidator:
    def __init__(self):
        pass

    def validate(self, data):
        raise NotImplementedError("Abstract method")

    def parse(self, data):
        raise NotImplementedError("Abstract method")
