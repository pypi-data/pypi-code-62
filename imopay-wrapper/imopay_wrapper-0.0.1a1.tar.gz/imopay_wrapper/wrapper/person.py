from .base import BaseImopayWrapper
from ..models.person import Person


class PersonWrapper(BaseImopayWrapper):
    """
    Wrapper para os métodos de person
    """

    @property
    def model(self):
        return Person

    @property
    def action(self):
        return "persons"
