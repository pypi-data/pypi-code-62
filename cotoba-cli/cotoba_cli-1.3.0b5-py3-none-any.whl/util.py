import requests

from cotoba_cli.error import ApiResponseError


def _handle_requests_exception(response, *args, **kwargs):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ApiResponseError(
            status_code=e.response.status_code, body=e.response.text)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)


def api_session(handle_error=True):
    session = requests.Session()
    if handle_error:
        session.hooks = {
            'response': _handle_requests_exception
        }
    return session
