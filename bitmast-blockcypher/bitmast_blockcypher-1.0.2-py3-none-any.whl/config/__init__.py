import configparser
import os
import re


class ConfigManager:
    __slots__ = '_name', '_config', '_path'

    def __init__(self, name: str, config_file: str = None, **kwargs):
        configs = ['block_cypher', 'config', 'crypto_currency']
        if name not in configs:
            raise RuntimeError('Named configuration not in registry')

        self._name = name
        self._path = None
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        if config_file is not None and isinstance(config_file, str):
            try:
                if os.path.isfile(config_file):
                    self._path = config_file
                    config.read(config_file)
            except IOError:
                raise
            except Exception:
                raise
        else:
            config_name = name.lower()
            path = os.path.join(os.path.dirname(__file__), config_name)
            path += '.ini'
            if os.path.isfile(path):
                self._path = path
                config.read(path)

        if kwargs:
            # update the configuration with dynamic settings
            # existing section will be overridden but defaults remains
            # restrict dynamic entries to only alphanumeric characters
            config.update({k: v for k, v in kwargs.items() if isinstance(k, str)
                           and isinstance(v, str) and v.isalnum()})
        self._config = config

    def option(self, section: str, option: str):
        if self._config.has_option(section, option):
            return self._config.get(section, option)

    def configurations(self):
        return self._config.sections()

    def get_by_value(self, section: str, option: str):
        out = self.option(section, option)
        int_pattern = re.compile(r'(\d+)')
        float_pattern = re.compile(r'(\d+)\.(\d+)')
        false_pattern = ('false', 'False', 'no', 'No', 'null', 'none', 'None')
        truth_pattern = ('true', 'Truth', 1)
        try:
            # parse out to sequence, int, float, str, None, bool
            if not out:
                raise ValueError('Specified entry not in configuration. Got: %s' % out)

            value = out.lower().strip()
            if value == 'none':
                return None
            elif int_pattern.match(value):
                return int(value)
            elif float_pattern.match(value):
                return float(value)
            elif value in false_pattern:
                return False
            elif value in truth_pattern:
                return True
            else:
                if ',' in out:
                    return out.split(',')
                else:
                    return out
        except Exception:
            raise

    @property
    def sections(self):
        return self._config.sections()

    @property
    def configuration(self):
        return self._name

    @property
    def path(self):
        return self._path


block_cypher_config = ConfigManager(name='block_cypher')

user_config = ConfigManager(name='config')

crypto_currency_config = ConfigManager(name='crypto_currency')
