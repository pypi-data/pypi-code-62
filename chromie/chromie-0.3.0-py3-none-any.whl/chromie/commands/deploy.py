from urllib import request, parse
from urllib import parse, error
import json
import time

import jwt

from config import Config


class AuthenticationError(Exception):
    pass


class BaseServiceAuth:
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    SCOPES = []

    def __init__(self, credentials={}):
        self._creds = credentials

    def service_token(self, email: str):
        data = {
            "grant_type": "urn:ietf:params:oath:grant-type:jwt-bearer",
            assertion: self._encode_token(email),
        }
        encoded = parse.urlencode(data)
        req = request.Request(TOKEN_URI, data=data)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        r = request.urlopen(req)
        return json.loads(r.text)

    def _encode_token(self, email: str):
        try:
            iat = round(time.time())
            exp = iat + 60
            payload = {
                "iss": self.credentials.get("client_email", None),
                "sub": email,
                "scope": " ".join(self.SCOPES) if len(self.SCOPES) > 0 else "",
                "exp": exp,
                "iat": iat
            }
            return jwt.encode(
                payload, self.credentials.get("private_key", None), algorithm="RS256"
            )
        except TypeError as e:
            raise AuthenticationError(e)

    @property
    def credentials(self):
        return self._creds

    def set_credentials(self, **kwargs):
        for k, v in kwargs.items():
            self._creds[k] = v



def main():

    with open("secrets.json", "r") as file:
        SECRETS = json.load(file)

    class GoogleStoreServiceAuth(BaseServiceAuth):
        SCOPES =[
            "https://www.googleapis.com/auth/gmail.settings.basic",
            "https://www.googleapis.com/auth/gmail.settings.sharing",
        ]

    config = {
        "private_key": SECRETS.private_key,
        "client_email": SECRETS.client_email
    }

    auth = GoogleStoreServiceAuth()
    auth.set_credentials(**config)

    try:
        token_dict = auth.service_token("steffen@andersland.dev")
        access_token = token_dict["access_token"]
        print(access_token)

    except AuthenticationError as e:
        print("AUTH ERROR: Please check your config.")
    # ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE
    
    # url = 'https://accounts.google.com/o/oauth2/auth'
    # params = {
    #     'response_type': 'code',
    #     'scope': 'https://www.googleapis.com/auth/chromewebstore',
    #     'client_id': '100634629910954449815',
    #     'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
    # }
    # data = parse.urlencode(params)
    # print(data)
    # encoded = data.encode('utf-8')
    # req = Request(url, encoded)

    # try:
    #     r = urlopen(req, context=ctx)
    # except error.HTTPError as e:
    #     if e.status != 307:
    #         raise Error("whelp...")
    #     redirected_url = parse.urljoin(url, e.headers['Location']) + '&' + data
    #     print(redirected_url)
    #     webbrowser.open(redirected_url)



if __name__ == '__main__':
    main()