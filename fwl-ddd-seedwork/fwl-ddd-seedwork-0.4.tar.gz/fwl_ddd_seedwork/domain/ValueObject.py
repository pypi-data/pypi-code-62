import abc

from fwl_ddd_seedwork.domain.DomainExceptions import ValueObjectError
from fwl_ddd_seedwork.domain.ValidationRule import ValidationRule


class ValueObject(abc.ABC):
    _DEFAULT_NAME: str = ""

    def __init__(self, def_name: str = ""):
        self._DEFAULT_NAME = def_name

    def _check_rule(self, validator: ValidationRule):
        if not validator.is_valid():
            raise ValueObjectError(self._DEFAULT_NAME, validator.message)
