from __future__ import print_function

import os
import sys
import logging
import logging.config


# Logging format example:
# 2018/11/20 12:36:37 INFO mlflow.sagemaker: Creating new SageMaker endpoint
LOGGING_LINE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOGGING_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

QUBOLE_HANDLER_LOG_FILE = "QUBOLE_HANDLER_LOG_FILE"
DEFAULT_QUBOLE_HANDLER_LOG_FILE = "/tmp/mlflow_internal.log"


def _configure_mlflow_loggers(root_module_name):
    qubole_handler_log_file = os.getenv(
        QUBOLE_HANDLER_LOG_FILE,
        DEFAULT_QUBOLE_HANDLER_LOG_FILE
    )

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'mlflow_formatter': {
                'format': LOGGING_LINE_FORMAT,
                'datefmt': LOGGING_DATETIME_FORMAT,
            },
        },
        'handlers': {
            'mlflow_handler': {
                'level': 'INFO',
                'formatter': 'mlflow_formatter',
                'class': 'logging.StreamHandler',
                'stream': sys.stderr,
            },
            'qubole_handler': {
                'level': 'INFO',
                'formatter': 'mlflow_formatter',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': qubole_handler_log_file,
                'maxBytes': 10240,
                'backupCount': 4
            }
        },
        'loggers': {
            root_module_name: {
                'handlers': ['mlflow_handler'],
                'level': 'INFO',
                'propagate': False,
            },
            '': {  # root logger
                'handlers': ['qubole_handler'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    })


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
