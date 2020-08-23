## Copyright (c) 2020 mangalbhaskar.
"""Logging configuration.

References:
* https://docs.python.org/3/howto/logging-cookbook.html#an-example-dictionary-based-configuration
* https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging
"""
__author__ = 'mangalbhaskar'

import os

_PYBOOZO_LOG_LEVEL_ = os.getenv('_PYBOOZO_LOG_LEVEL_')

_PYBOOZO_LOG_LEVEL_ = _PYBOOZO_LOG_LEVEL_.upper() if _PYBOOZO_LOG_LEVEL_ \
                        and _PYBOOZO_LOG_LEVEL_ in ['CRITICAL','ERROR','WARNING','INFO','DEBUG','NOTSET'] \
                            else 'ERROR'
print('_PYBOOZO_LOG_LEVEL_ is: {}'.format(_PYBOOZO_LOG_LEVEL_))

logcfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            # 'format': '%(levelname)s %(message)s'
            'format': '[%(levelname)s]:[%(filename)s:%(lineno)d - %(funcName)20s() ]: %(message)s'
            # 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'standard': { 
            # 'format': '%(asctime)s:[%(levelname)s]:%(lineno)d:%(name)s:: %(message)s'
            'format': '%(asctime)s:[%(levelname)s]:[%(name)s]:[%(filename)s:%(lineno)d - %(funcName)20s() ]: %(message)s'
        },
    },
    'filters': {},
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        # 'file_info': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'level': 'DEBUG',
        #     'formatter': 'standard',
        #     'filename': '.boozo.log',
        #     'maxBytes': 10485760,
        #     # 'maxBytes': 10,
        #     # 'backupCount': 20,
        #     'encoding': 'utf8'
        # },
        # 'file_error': {
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'level': 'ERROR',
        #     'formatter': 'standard',
        #     'filename': 'log/errors.log',
        #     'maxBytes': 10485760,
        #     'backupCount': 20,
        #     'encoding': 'utf8'
        # }
    },
    'loggers':{
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {
            'handlers': ['console'],
            # 'handlers': ['file_info'],
            # 'level': 'CRITICAL',
            # 'level': 'ERROR',
            # 'level': 'WARNING',
            # 'level': 'INFO',
            # 'level': 'DEBUG',
            # 'level': 'NOTSET',
            'propagate': False
        }
    }
}

logcfg['loggers']['__main__']['level'] = _PYBOOZO_LOG_LEVEL_
