import os

import yaml


SUPPORT_TYPES = {
    str: ['string'],
    int: ['integer'],
    float: ['float', 'double'],
    bool: ['boolean'],
    list: ['list', 'array'],
    dict: ['dict', 'object'],
}

SUPPORT_TYPES_INDEX = { name: t 
    for t, names in SUPPORT_TYPES.items() for name in names }


def convert(type_, value, default):
    value = value.strip()
    if value == '':
        return default
    result = yaml.safe_load(value)
    if isinstance(result, SUPPORT_TYPES_INDEX.get(type_, str)):
        return result
    return value


class Settings:

    def __init__(self, filepath=None):
        self.schema = {}
        self.load(filepath)

    def load(self, filepath=None):
        if not filepath:
            return
        filepath, nodepath = (filepath.split('#', 1) + [''])[:2]
        content = yaml.safe_load(open(filepath))
        for p in nodepath.split('.'):
            content = content.get(p)
        self.schema = content

    def get(self, key, default=None):
        if key not in self.schema:
            return os.getenv(key, default)
        type_ = self.schema[key].get('type', str)
        value = self.schema[key].get('default', None)
        if key in os.environ:
            return convert(type_, os.getenv(key), default)
        return value


_ins = None

def instance():
    global _ins
    if _ins is None:
        _ins =  Settings(os.getenv('FENDA_SETTINGS'))
    return _ins


def get(key, default=None):
    return instance().get(key, default)

def load(filepath=None):
    return instance().load(filepath)
