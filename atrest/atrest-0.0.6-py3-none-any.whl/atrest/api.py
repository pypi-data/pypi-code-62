import requests, os
from requests import exceptions
from pprint import pprint as p
import json
from .config import Config

class API():

    def __init__(self):
        self.config = Config()
         
        self.base_url = os.getenv("AT_BASE_URL")

        self.api_integration_code = os.getenv("AT_INTEGRATION_CODE")
        self.username = os.getenv("AT_USERNAME")
        self.secret = os.getenv("AT_SECRET")

        self.headers = {
            "ApiIntegrationCode": self.api_integration_code,
            "UserName": self.username,
            "Secret": self.secret,
            "Content-Type": "application/json",
        }


    def get_base_url(self):
        return self.base_url


    def set_base_url(self, base_url):
        self.base_url = base_url


    def get_headers(self):
        return self.headers


    def set_headers(self, api_integration_code=None, username=None, secret=None):
        dictionary = {
            "api_integration_code": "ApiIntegrationCode",
            "username": "UserName",
            "secret": "Secret",
        }

        to_set = {}

        for k, v in locals().items():
            if k == "self" or k == "dictionary" or k == "to_set":
                continue
            elif v == None:
                continue
            else:
                key = dictionary.get(k, "")
                if key == "":
                    raise(Exception)
                elif v == "":
                    raise(ValueError)
                else:
                    to_set[key] = v

        for k, v in to_set.items():
            self.headers[k] = v

        return self.headers 


    def query_tickets(self) -> requests.Response:
        try:
            resp = requests.get(self.base_url + '/Tickets/query?search={"filter":[{"op":"contains","field":"Title","value":"Infected"}]}', headers=self.headers)
            resp.raise_for_status()
            return resp
        except exceptions.HTTPError as e:
            raise e


    def create_ticket(self, title, description, status, priority, company_id, queue_id):
        
        data = {
            "Title": title,
            "Description": description,
            "Status": status, # 1
            "Priority": priority, # 1
            "CompanyID": company_id, # 0
            "QueueID": queue_id, # 29682833 
        }

        payload = json.dumps(data)
        try:
            resp = requests.post(self.base_url + '/Tickets', headers=self.headers, data=payload)
            resp.raise_for_status()
            return resp
        except exceptions.HTTPError as e:
            raise e