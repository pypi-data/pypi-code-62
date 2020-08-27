from unittest.mock import MagicMock
from tests.base import BaseTest


class TestCardPayment(BaseTest):
    def test_card_payment(self):
        kwargs = dict(
            sid=self.sid, vid=self.vid, curr=self.currency, cardn="12345678",
            cvv="123", month="12", year="2020", cust_address="Billing, Address",
            cust_city="City", cust_country="Country", cust_postcode="0000",
            cust_stateprov="State/Province", fname="fname", lname="lname"
        )
        data = {
            "txncd": "1111111122", "qwh": "1000988633", "afd": "827071654",
            "poi": "1211883119", "uyt": "1431931896", "ifd": "548464895",
            "agt": "", "id": "oid", "status": "bdi6p2yy76etrs", "ivm": "oid",
            "mc": "100", "p1": "", "p2": "", "p3": "", "p4": "",
            "msisdn_id": "John Doe", "msisdn_idnum": "123456",
            "msisdn_custnum": "123456", "channel": "Credit_Card",
            "card_mask": "444444xxxxxx4444"}
        self.instance.card_payment_request = MagicMock(
            return_value=data)
        response = self.instance.card_payment_request(**kwargs)
        assert response == data
