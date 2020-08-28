from unittest.mock import MagicMock
from tests.base import BaseTest


class TestCardPayment(BaseTest):
    def test_payment_status(self):
        kwargs = dict(
            oid=self.order_id, vid=self.vid
        )
        data = {
            "header_status": 200,
            "status": 1,
            "text": "payment record found",
            "data": {
                "vid": "demo",
                "session_id": "852a63b08ac98b1750498rfd7c547c8d",
                "oid": "34b674",
                "transaction_amount": "200.00",
                "transaction_code": "TXNCODE",
                "telephone": "2547XXXXXXXX",
                "firstname": "JOHN",
                "lastname": "DOE",
                "paid_at": "2016-05-14 16:13:50",
                "payment_mode": "MPESA"
            },
            "hash": "d29ac43a8b89673cc85ce206351832d3a0c4a462dd0fde56c17445e94f6ad958"
        }
        self.instance.payment_status_request = MagicMock(
            return_value=data)
        response = self.instance.payment_status_request(**kwargs)
        assert response["status"] == 1
