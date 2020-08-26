import json, os
from google.cloud import iam_credentials
from datetime import datetime, timedelta

class GCPOIDCClient:

    @property
    def client_email(self):
        return self._client_email

    @property
    def audience(self):
        return 'NA' if self._audience is None else self._audience

    @property
    def expiry(self):
        return self._expiry

    def __init__(self, options=None):
        
        self._client_email = None
        self._audience = None
        self._expiry = None
        self._debug = False
        self._token = None        

        options = {} if options is None else options
        options['caller_service_account_file'] = options.get("caller_service_account_file")
        options['client_service_account_file'] = options.get('client_service_account_file')
        options['client_service_account_email'] = options.get('client_service_account_email')
        options['debug'] = options.get('debug', False)

        self._debug = options['debug']

        default_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        caller_service_account_file = options.get("caller_service_account_file")
        client_service_account_file = options.get('client_service_account_file')
        client_service_account_email = options.get('client_service_account_email')

        if caller_service_account_file:
            self.client = iam_credentials.IAMCredentialsClient.from_service_account_file(caller_service_account_file)
        else:
            self.client = iam_credentials.IAMCredentialsClient()

        if client_service_account_email:
            self._client_email = client_service_account_email
        else:
            if client_service_account_file:
                self._client_email = self.get_client_email_for_caller_service_account_file(client_service_account_file)
            elif caller_service_account_file:
                self._client_email = self.get_client_email_for_caller_service_account_file(caller_service_account_file)
            else:
                self._client_email = self.get_client_email_for_caller_service_account_file(default_credentials)

    def _log(self, msg):
        if self._debug:
            print("[x] {}".format(msg))

    def get_client_email_for_caller_service_account_file(self, service_account_file=None):
        if service_account_file is None:
            return None
            
        with open(service_account_file) as json_file:
            data = json.load(json_file)
            return data['client_email']

    def refresh_id_token(self, options=None):
        options = {} if options is None else options
        options['service_account_id'] = options.get('service_account_id', self.client_email)
        options['audience'] = options.get('audience', self.audience)

        service_account = options.get('service_account_id')
        if service_account is None:
            raise Exception("A service account email or unique id is required to generate an id token")

        self._log("Preparing to refresh token for {}".format(options))
        
        name = 'projects/-/serviceAccounts/{}'.format(service_account)
        audience = options['audience']
        response = self.client.generate_id_token(name=name, audience=audience, delegates=None, include_email=True, retry=None)
        self._token = None if response is None else response.token
        self._expiry = datetime.utcnow() + timedelta(minutes=59)
        self._log("Token was successfully refreshed. It expires at {}".format(self.expiry))

    def get_id_token(self):
        due_for_refresh = not self._token or (datetime.utcnow() > self._expiry)
        if due_for_refresh:
            self.refresh_id_token()
        return self._token