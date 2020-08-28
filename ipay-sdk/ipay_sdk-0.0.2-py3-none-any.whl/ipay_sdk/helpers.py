from hashlib import sha1, sha256
import logging
import requests
import hmac

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make_request(**kwargs):
    try:
        req = requests.request(**kwargs)
    except Exception as e:
        logger.exception("Request Error: {}".format(str(e)))
        return None
    else:
        return req


def create_signature(secret_key, string, is_256=False):
    """Create signature"""
    string_to_sign = string.encode('utf-8')
    hashed = hmac.new(secret_key, string_to_sign, sha256 if is_256 else sha1)
    return hashed.hexdigest()
