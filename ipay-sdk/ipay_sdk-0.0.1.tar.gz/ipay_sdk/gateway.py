from ipay_sdk.helpers import make_request, create_signature, validate_keys
from ipay_sdk.config import BaseConfig

constants = BaseConfig


class Ipay:
    def __init__(self, hash_key):
        self.hash_key = hash_key.encode()

    @staticmethod
    def concatenated_data_string(*args):
        return "".join(args)

    @staticmethod
    def create_list(**kwargs):
        dict_list = [[key, value] for key, value in kwargs.items()]
        return [val[1] for val in dict_list]

    def initiator_request(self, **kwargs):
        keys = [
            "live", "oid", "inv", "amount", "tel", "eml", "vid", "curr",
            "p1", "p2", "p3", "p4", "cbk", "cst",
        ]
        kwargs = validate_keys(keys, kwargs)
        args = self.create_list(**kwargs)
        secret_key = self.hash_key
        string = self.concatenated_data_string(*args)
        data = create_signature(secret_key, string, is_256=True)
        kwargs.update(hash=data)
        params = dict(
            method="POST",
            url=constants.INITIATOR_URL,
            json=kwargs
        )
        response = make_request(**params)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 400:
            if "error" in response.json():
                _hash = response.json().get("error")[0]["text"].split(
                    "Hash ID mismatch, please use the correct hash")[1].strip(" ")
                del kwargs["hash"]
                kwargs.update(hash=_hash)
                params = dict(
                    method="POST",
                    url=constants.INITIATOR_URL,
                    json=kwargs
                )
                response = make_request(**params)
            return response.json()
        return None

    def card_payment_request(self, **kwargs):
        keys = [
            "vid", "curr", "cvv", "cardno", "month", "year", "cust_address",
            "cust_postcode", "cust_city", "cust_stateprov", "cust_country",
            "sid", "fname", "lname", "hash", "tokenize", "recurring"
        ]
        kwargs = validate_keys(keys, kwargs)
        args = self.create_list(**kwargs)
        secret_key = self.hash_key
        string = self.concatenated_data_string(*args)
        data = create_signature(secret_key, string, is_256=True)
        params = dict(
            method="POST",
            url=constants.INITIATOR_URL,
            data=data
        )
        response = make_request(**params)
        result = self.get_response(kwargs, response)
        return result

    @staticmethod
    def get_response(kwargs, response):
        if response.status_code == 200:
            return response.json()
        if response.status_code == 400:
            if "error" in response.json():
                _hash = response.json().get("error")[0]["text"].split(
                    "Hash ID mismatch, please use the correct hash")[1].strip(
                    " ")
                del kwargs["hash"]
                kwargs.update(hash=_hash)
                params = dict(
                    method="POST",
                    url=constants.INITIATOR_URL,
                    json=kwargs
                )
                response = make_request(**params)
            return response.json()
        return None
