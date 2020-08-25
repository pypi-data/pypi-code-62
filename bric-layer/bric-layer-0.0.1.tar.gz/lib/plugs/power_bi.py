import requests
import adal


class PowerBIAPI:
    def __init__(self, layer):
        self.layer = layer

    def obtain_token(self, username, password):
        context = adal.AuthenticationContext(
            authority=self.layer.config.connections.power_bi.authority_url,
            validate_authority=True,
            api_version=None)

        token = context.acquire_token_with_username_password(
            resource=self.layer.config.connections.power_bi.resource_url,
            client_id=self.layer.config.connections.power_bi.client_id,
            username=username,
            password=password)

        return token.get('accessToken')

    def build_refresh_url(self, group_id, dataset_key, username, password):
        refresh_url = self.layer.config.connections.power_bi.base_uri.format(group_id, dataset_key)

        header = {'Authorization': 'Bearer {}'.format(self.obtain_token(username, password))}
        return refresh_url, header

    def refresh_dataset(self, group_id, dataset_key, username, password):
        refresh_url, header = self.build_refresh_url(group_id, dataset_key, username, password)

        try:
            requests.post(refresh_url, headers=header)
        except ConnectionError as e:
            raise Exception(e)

    def check_refresh_status(self, group_id, dataset_key, username, password):
        refresh_url, header = self.build_refresh_url(group_id, dataset_key, username, password)

        refresh_response = requests.get(refresh_url, headers=header)

        try:
            return refresh_response.json()['value'][0]['status']
        except ValueError:
            self.layer.log.error('Refresh unsuccessful')
            return None
