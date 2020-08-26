from .address import AddressWrapper
from .company import CompanyWrapper
from .person import PersonWrapper


class ImopayWrapper:
    def __init__(self):
        self.address = AddressWrapper()
        self.company = CompanyWrapper()
        self.person = PersonWrapper()
