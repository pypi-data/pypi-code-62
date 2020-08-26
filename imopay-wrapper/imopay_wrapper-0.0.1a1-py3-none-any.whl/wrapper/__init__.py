from .address import AddressWrapper
from .company import CompanyWrapper
from .person import PersonWrapper


class ImopayWrapper:
    def __init__(self, *args, **kwargs):
        self.address = AddressWrapper(*args, **kwargs)
        self.company = CompanyWrapper(*args, **kwargs)
        self.person = PersonWrapper(*args, **kwargs)
