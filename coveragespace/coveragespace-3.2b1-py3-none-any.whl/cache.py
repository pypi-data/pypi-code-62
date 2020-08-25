import os
import pickle

import log


class Cache:

    PATH = os.path.join('.cache', 'coveragespace')

    def __init__(self):
        self._data = {}

    def _store(self):
        directory = os.path.dirname(self.PATH)
        if not os.path.exists(directory):
            os.makedirs(directory)

        text = pickle.dumps(self._data)
        with open(self.PATH, 'wb') as fout:
            fout.write(text)

    def _load(self):
        try:
            with open(self.PATH, 'rb') as fin:
                text = fin.read()
        except IOError as e:
            log.debug("Unable to read cache: %s", e)
            return

        try:
            data = pickle.loads(text)
        except (TypeError, KeyError, IndexError) as e:
            log.debug("Unable to parse cache: %s", e)

        if isinstance(data, dict):
            self._data = data
        else:
            log.debug("Invalid cache value: %s", data)
            self._data = {}

    def set(self, key, value):
        slug = self._slugify(key)
        log.debug("Setting cache key: %s", slug)
        self._data[slug] = value
        log.debug("Cached value: %s", value)
        self._store()

    def get(self, key, default=None):
        self._load()
        slug = self._slugify(key)
        log.debug("Getting cache key: %s", slug)
        value = self._data.get(slug, default)
        log.debug("Cached value: %s", value)
        return value

    def clear(self):
        self._data = {}
        self._store()

    @staticmethod
    def _slugify(key):
        try:
            url, data = key
        except ValueError:
            return key
        else:
            return url, tuple(data.items())
