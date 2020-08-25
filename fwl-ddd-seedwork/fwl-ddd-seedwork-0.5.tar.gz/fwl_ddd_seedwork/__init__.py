# __init__.py

# Version of the realpython-reader package
__version__ = "0.5"

from .domain import Entity, ValueObject, ValidationRule, DomainError, ValueObjectError
from .dto import DTO
from .mapper import BaseMapper
from .infrastructure import Schema
