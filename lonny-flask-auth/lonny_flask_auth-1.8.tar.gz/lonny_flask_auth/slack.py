import requests
from flask import request, redirect
from furl import furl
from .base import Strategy

ACCESS_URL = "https://slack.com/api/oauth.v2.access"
AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
PROTO_HEADER = "X-Forwarded-Proto"

class SlackStrategy(Strategy):
    def __init__(self, client_id, client_secret, *, scope):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope

    def _get_current_url(self):
        parsed = furl(request.url)
        # Deals with the scenario that the protocol is HTTP
        # due to termination of the HTTPS request at the load balancer.
        if PROTO_HEADER in request.headers:
            parsed.scheme = request.headers[PROTO_HEADER]
        return parsed.url

    def _get_authorize_url(self):
        parsed = furl(AUTHORIZE_URL)
        parsed.args = dict(
            client_id = self._client_id,
            scope = self._scope,
            redirect_uri = self._get_current_url()
        )
        return parsed.url

    def _get_access_data(self, code):
        parsed = furl(self._get_current_url())
        parsed.args = dict()
        resp = requests.post(ACCESS_URL, data = dict(
            code = code,
            client_id = self._client_id,
            client_secret = self._client_secret,
            redirect_uri = parsed.url
        ))
        if resp.status_code == 200:
            data = resp.json()
            if data["ok"]:
                return data

    # Default behaviour is to just return the access token payload
    # as the "user".
    def get_user(self, data):
        return data

    def authenticate(self, state):
        state.attempted = True
        if "code" not in request.args:
            return redirect(self._get_authorize_url())
        data = self._get_access_data(request.args["code"])
        if data is None:
            return 
        state.user = self.get_user(data)