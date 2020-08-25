
import copy
import os
import requests
import json
import datetime
from urllib.parse import urljoin

class FinieAPI:
    
    def __init__(self, url='https://finieservices.uatisbank/'):
        self.url = url
        self.session = requests.Session()
        self.session.verify = False
        
        self.data = {
            "query": "",
            "lat": "",
            "lon": "",
            "inputtype": "",
            "time_offset": 300,
            "classifier": "stateful-isbank-states-state",
            "dialog": "finie_session_start",
            "device": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
        }
        
        self.login()
    
    def login(self,):
        
        url = f'{self.url}v1/oauth/'
        params = "client_id=rKVJ1uEgfviTOc4BfXC5CyUgJD9VYxsvtyJxiCrT&client_secret=tvYCuNq2mB5xLgKChkSyehFA83YjIfqbmYZNYGDkcLUyw6BKITDRKQjiT5N7ynexNPbHc2UoMI2VosYtwLzT3CCL5MjAMaFX2k6wm8pGYS5JPcLo4Mew6jIQi1edLqHr&grant_type=client_credentials&clinc_user_id=161215276"
        data = dict([p.split('=') for p in params.split('&')])
        # resp = requests.post(url, data = data, verify=False )
        resp = self.session.post(url, data = data)
        self.access_token = resp.json()['access_token']
        self.session.headers.update(
            {
                'Authorization': f'Bearer {self.access_token}',
                'Accept': 'application/json'
            }
        )
        
        print(f'Login {resp.status_code} {self.access_token}')
        
        
    def query(self, text):
        url = f'{self.url}v1/query/'
        self.data['query'] = text
        resp =  self.session.post(url, json=self.data).json()

        if resp == {'detail': 'Using expired access token.'}:
            print('token is expired.')
            self.login()
            print('new token is obtained.')
            return self.query(text)
        else:
            return resp