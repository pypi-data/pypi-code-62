import logging
import traceback

from skywalking import Layer, Component, agent
from skywalking.trace import tags
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import Tag
from skywalking import config

logger = logging.getLogger(__name__)


def install():
    try:
        from requests import Session

        _request = Session.request

        def _sw_request(this: Session, method, url,
                        params=None, data=None, headers=None, cookies=None, files=None,
                        auth=None, timeout=None, allow_redirects=True, proxies=None,
                        hooks=None, stream=None, verify=None, cert=None, json=None):

            from urllib.parse import urlparse
            url_param = urlparse(url)

            if config.protocol == 'http' and config.collector_address.rstrip('/').endswith(url_param.netloc):
                return _request(this, method, url, params, data, headers, cookies, files, auth, timeout,
                                allow_redirects,
                                proxies,
                                hooks, stream, verify, cert, json)

            context = get_context()
            carrier = Carrier()
            with context.new_exit_span(op=url_param.path or "/", peer=url_param.netloc, carrier=carrier) as span:
                span.layer = Layer.Http
                span.component = Component.General

                if agent.connected():
                    if headers is None:
                        headers = {}
                        for item in carrier:
                            headers[item.key] = item.val
                    else:
                        for item in carrier:
                            headers[item.key] = item.val

                try:
                    res = _request(this, method, url, params, data, headers, cookies, files, auth, timeout,
                                   allow_redirects,
                                   proxies,
                                   hooks, stream, verify, cert, json)

                    span.tag(Tag(key=tags.HttpMethod, val=method.upper()))
                    span.tag(Tag(key=tags.HttpUrl, val=url))
                    span.tag(Tag(key=tags.HttpStatus, val=res.status_code))
                    if res.status_code >= 400:
                        span.error_occurred = True
                except BaseException as e:
                    span.raised()
                    raise e
                return res

        Session.request = _sw_request
    except Exception:
        logger.warning('failed to install plugin %s', __name__)
        traceback.print_exc()
