# -*- coding: utf-8 -*-
import os
import oyaml as yaml

from collections import OrderedDict

from .exceptions import ODRouteConfigException

DEFAULT_CONFIG = {
    'name': None,
    'source_ports': [],
    'destinations': [],
    'nodata_failover_delay': 0.5,
    'nodata_recover_delay': 5,
    'noaudio_failover_delay': 10,
    'noaudio_recover_delay': 10,
    'audio_threshold': -90,
    'telnet': None,
    'socket': None,
    'log_level': 'INFO',
    'log_format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
}


def load_config_file(path):
    if not os.path.exists(path):
        raise IOError('Config file does not exist: {}'.format(path))

    with open(path, 'r') as config_file:
        config = yaml.load(config_file)

    if not config:
        raise ODRouteConfigException('Unable to read configuration from file')

    parsed_config = parse_config(config)
    parsed_config['config_file'] = path

    return parsed_config


def parse_config(config):
    parsed_config = OrderedDict()

    defaults = OrderedDict(sorted(DEFAULT_CONFIG.items()))

    for key, value in defaults.items():
        """
        kind of ugly handling. make sure to apply default values if config file has
        keys set to 'none' - like:
            ...
            source_ports:
             - 7000
            destinations:
            nodata_failover_delay: 1.0
            ...
        """
        _value = config.get(key, value)
        if not _value:
            _value = value

        parsed_config[key] = _value

    # handle logging config
    parsed_config['log_level'] = parsed_config['log_level'].upper()

    if parsed_config['name']:
        parsed_config['log_format'] = 'odroute-{} {}'.format(parsed_config['name'], parsed_config['log_format'])

    if parsed_config['socket']:
        parsed_config['socket'] = os.path.abspath(parsed_config['socket'])

    return parsed_config
