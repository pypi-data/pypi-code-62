"""StoredSafe API wrapper module."""
from pathlib import Path
import requests

class RCException(Exception):
    """Failed to read rc file."""

class ApikeyUndefinedException(Exception):
    """Cannot authenticate with StoredSafe API calls because apikey is not defined."""


class TokenUndefinedException(Exception):
    """Cannot use privileged StoredSafe API calls because token is not defined."""


# pylint: disable=too-many-public-methods
class StoredSafe:
    """StoredSafe API wrapper class."""

    @staticmethod
    def from_rc(path=Path.home() / '.storedsafe-client.rc'):
        """Create StoredSafe instance from rc-file"""
        config = {}
        try:
            with Path(path).open('r') as rc_file:
                for line in rc_file:
                    [key, value] = line.strip().split(':')
                    if key == 'mysite':
                        config['host'] = value
                    elif key == 'apikey':
                        config['apikey'] = value
                    elif key == 'token':
                        config['token'] = value
        except:
            raise RCException()
        return StoredSafe(**config)

    def __init__(self, host, apikey=None, token=None, version='1.0'):
        self.host = host
        self.apikey = apikey
        self.token = token
        self.api_version = version

    ###
    # Helper methods.
    ##
    def __assert_apikey_exists(self):
        """Throws ApikeyUndefinedException if token is None."""
        if self.apikey is None:
            raise ApikeyUndefinedException()

    def __auth(self, data):
        """Authenticate with StoredSafe and save token if the request was successful."""
        self.__assert_apikey_exists()
        res = requests.post(self.__get_url('/auth'), json=data)
        if res.status_code == 200:
            data = res.json()
            self.token = data['CALLINFO']['token']
        return res

    def __headers(self):
        """Create the required headers for requests to the StoredSafe API."""
        self.__assert_token_exists()
        return {'X-Http-Token': self.token}

    def __assert_token_exists(self):
        """Throws TokenUndefinedException if token is None."""
        if self.token is None:
            raise TokenUndefinedException()

    def __get_url(self, path):
        """Get the full url of the relative API path."""
        return f'https://{self.host}/api/{self.api_version}/{path.strip("/")}'

    def __get(self, path, params=None):
        """Send a GET request to the provided relative API path."""
        self.__assert_token_exists()
        if params is None:
            return requests.get(self.__get_url(path), headers=self.__headers())
        return requests.get(self.__get_url(path), params=params, headers=self.__headers())

    def __post(self, path, data):
        """Send a POST request to the provided relative API path."""
        self.__assert_token_exists()
        return requests.post(self.__get_url(path), json=data, headers=self.__headers())

    def __put(self, path, data):
        """Send a PUT request to the provided relative API path."""
        self.__assert_token_exists()
        return requests.put(self.__get_url(path), json=data, headers=self.__headers())

    def __delete(self, path):
        """Send a DELETE request to the provided relative API path."""
        self.__assert_token_exists()
        return requests.delete(self.__get_url(path), headers=self.__headers())

    ###
    # API Auth methods.
    ##
    def login_totp(self, username, passphrase, otp):
        """Request login using TOTP."""
        data = {
            'username': username,
            'passphrase': passphrase,
            'otp': otp,
            'apikey': self.apikey,
            'logintype': 'totp',
        }
        return self.__auth(data)

    def login_yubikey(self, username, passphrase, otp):
        """Request login using Yubico OTP."""
        data = {
            'username': username,
            'keys': f'{passphrase}{self.apikey}{otp}',
            'apikey': self.apikey,
        }
        return self.__auth(data)

    def logout(self):
        """Request logout."""
        return self.__get('/auth/logout')

    def check(self):
        """Request check status of session."""
        return self.__post('/auth/check', {})

    ###
    # API Vault methods.
    ##
    def list_vaults(self):
        """Request a list of all vaults."""
        return self.__get('/vault')

    def vault_objects(self, vault_id):
        """Request a list of the objects in a vault."""
        return self.__get(f'/vault/{vault_id}')

    def vault_members(self, vault_id):
        """Request a list of the members in a vault."""
        return self.__get(f'/vault/{vault_id}/members')

    def add_vault_member(self, vault_id, user_id, status):
        """Request to add a member to a vault."""
        return self.__post(f'/vault/{vault_id}/member/{user_id}', {'status': status})

    def edit_vault_member(self, vault_id, user_id, status):
        """Request to edit a member in a vault."""
        return self.__put(f'/vault/{vault_id}/member/{user_id}', {'status': status})

    def remove_vault_member(self, vault_id, user_id):
        """Request to remove a member from a vault."""
        return self.__delete(f'/vault/{vault_id}/member/{user_id}')

    def create_vault(self, **params):
        """Request the creation of a new vault."""
        return self.__post('/vault', params)

    def edit_vault(self, vault_id, **params):
        """Request an edit of an existing vault."""
        return self.__put(f'/vault/{vault_id}', params)

    def delete_vault(self, vault_id):
        """Request the deletion of a vault."""
        return self.__delete(f'/vault/{vault_id}')

    ###
    # API Object methods.
    ##
    def get_object(self, object_id, children=False):
        """Request a StoredSafe object and optionally its children."""
        return self.__get(f'/object/{object_id}', {'children': 'true' if children else 'false'})

    def decrypt_object(self, object_id):
        """Request the decryption of a StoredSafe object."""
        return self.__get(f'/object/{object_id}', {'decrypt': 'true'})

    def get_file(self, object_id):
        """Request a base64 string of a file object."""
        return self.__get(f'/object/{object_id}', {'decrypt': 'true', 'filedata': 'true'})

    def create_object(self, **params):
        """Request the creation of an object."""
        return self.__post('/object', params)

    def edit_object(self, object_id, **params):
        """Request the edit of an existing object."""
        return self.__put(f'/object/{object_id}', params)

    def delete_object(self, object_id):
        """Request the deletion of an object."""
        return self.__delete(f'/object/{object_id}')

    def find(self, needle):
        """Request all objects with searchable fields matching the needle."""
        return self.__get('/find', {'needle': needle})

    ###
    # API Templates methods.
    ##
    def list_templates(self):
        """Request a list of all available templates."""
        return self.__get('/template')

    def get_template(self, template_id):
        """Request a StoredSafe template."""
        return self.__get(f'/template/{template_id}')

    ###
    # API User methods
    ##
    def list_users(self, search_string=None):
        """Request list of all users or any users matching search string."""
        if search_string is None:
            return self.__get('/user')
        return self.__get(f'/user/{search_string}')

    def get_user(self, user_id):
        """Request user matching the user_id."""
        return self.__get(f'/user/{user_id}')

    def create_user(self, **params):
        """Request the creation of a new user."""
        return self.__post('/user', params)

    def edit_user(self, user_id, **params):
        """Request the creation of a new user."""
        return self.__put(f'/user/{user_id}', params)

    def delete_user(self, user_id):
        """Request the creation of a new user."""
        return self.__delete(f'/user/{user_id}')

    ###
    # API Utils methods.
    ##
    def status_values(self):
        """Request a list of all available capabilities and permission bits."""
        return self.__get('/utils/statusvalues')

    def password_policies(self):
        """Request a list of all available password policies."""
        return self.__get('/utils/policies')

    def version(self):
        """Request the version of the StoredSafe server."""
        return self.__get('/utils/version')

    def generate_password(self, **params):
        """Request a password generated with the passed settings (or vault policy)."""
        return self.__get('/utils/pwgen', params=params)
