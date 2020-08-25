"""API client functions."""


import time

import log
import requests

from .cache import Cache


cache = Cache()


def get(url, data):
    log.info("Getting %s: %s", url, data)

    response = cache.get((url, data))
    if response is None:
        for delay in [1, 3, 5]:
            response = requests.put(url, data=data)
            if response.status_code == 500:
                time.sleep(delay)
                continue
            break
        cache.set((url, data), response)

    log.info("Response: %s", response)

    return response


def delete(url, data):
    log.info("Deleting %s: %s", url, data)

    for delay in [1, 3, 5]:
        response = requests.delete(url, data=data)
        if response.status_code == 500:
            time.sleep(delay)
            continue
        break

    log.info("Response: %s", response)

    cache.clear()

    return response
