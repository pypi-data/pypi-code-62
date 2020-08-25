import json
import multiprocessing
from munch import Munch


# deep merge objects
def selective_merge(base_obj, delta_obj):
    if not isinstance(base_obj, dict):
        return delta_obj
    common_keys = set(base_obj).intersection(delta_obj)
    new_keys = set(delta_obj).difference(common_keys)
    for k in common_keys:
        base_obj[k] = selective_merge(base_obj[k], delta_obj[k])
    for k in new_keys:
        base_obj[k] = delta_obj[k]
    return base_obj


def get_json5(env='', bric=''):
    path = ('.{}{}/config/{}config.json5'
            .format('/brics/' if bric else '', bric, env + '_' if env and env != 'prod' else ''))

    json_file = open(path)
    config_file = json.load(json_file)
    json_file.close()

    return config_file


def set_env_variables(config, **env_vars):
    for key, value in env_vars.items():
        config['environment'][key] = value

    config['environment']['max_workers'] = multiprocessing.cpu_count() * 2 + 1

    # add additional environment variables here

    return config


def load_layer_config(env):
    # set prod config for prod environment
    default_json = get_json5()

    config_json = default_json.copy()

    default_json = Munch.fromDict(default_json)

    env = (default_json.environment[env] if env in default_json.environment
           else default_json.environment.default)

    # append dev config for dev and local environment
    if env != default_json.environment.prod:
        dev_json = get_json5(default_json.environment.dev)
        config_json = selective_merge(config_json, dev_json)

    # append local config for local environment
    if env == default_json.environment.local:
        local_json = get_json5(default_json.environment.local)
        config_json = selective_merge(config_json, local_json)

    return set_env_variables(config_json, current=env)


# TODO - all of this is terrible, redo it.
class Config(object):
    def __init__(self, env):
        for (key, value) in (load_layer_config(env)).items():
            self[key] = value

    def __setitem__(self, index, value):
        self.__dict__[index] = value

    def __getitem__(self, index):
        return self.__dict__[index]

    def load_bric_config(self, bric_name):
        # set prod config for prod environment
        default_json = get_json5(self['environment']['prod'], bric_name)

        config_json = default_json.copy()

        # append dev config for dev and local environment
        if self['environment']['current'] != self['environment']['prod']:
            dev_json = get_json5(self['environment']['dev'], bric_name)
            config_json = selective_merge(config_json, dev_json)

        # append local config for local environment
        if self['environment']['current'] == self['environment']['local']:
            local_json = get_json5(self['environment']['current'], bric_name)
            config_json = selective_merge(config_json, local_json)

        config_json = selective_merge(self.__dict__, config_json)

        return Munch.fromDict(config_json)
