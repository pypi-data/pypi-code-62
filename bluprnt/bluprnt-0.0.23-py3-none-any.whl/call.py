import os
import logging
from urllib.parse import urljoin
import requests

GCP_PROJECT = os.environ["GCP_PROJECT"]
FUNCTION_REGION = os.environ["FUNCTION_REGION"]


class ServiceResponse:
    def __init__(self, response: requests.Response):
        try:
            self.data = response.json()
        except ValueError:
            self.data = None
        self.raw_content = response.content
        self.status_code = response.status_code
        self.raise_for_status = response.raise_for_status


def get_auth_header(audience):
    token_url = (
        "http://metadata.google.internal"
        "/computeMetadata/v1/instance/service-accounts/default/identity"
        f"?audience={audience}"
    )
    token = requests.get(
        url=token_url, headers={"Metadata-Flavor": "Google"},
    ).content.decode()
    return {"Authorization": "Bearer " + token}


def call(name, **kwargs):
    url = f"https://{FUNCTION_REGION}-{GCP_PROJECT}.cloudfunctions.net/{name}"
    logging.info("CALL: %s %s", name, kwargs)
    r = requests.post(url, headers=get_auth_header(url), json=kwargs)
    service_resp = ServiceResponse(r)
    logging.info("RESPONSE: %s %s", service_resp.status_code, service_resp.data)
    return service_resp
