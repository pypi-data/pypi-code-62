from .base import BaseImopayWrapper
from ..models.company import Company


class CompanyWrapper(BaseImopayWrapper):
    """
    Wrapper para os métodos de company
    """

    @property
    def model(self):
        return Company

    @property
    def action(self):
        return "companies"
