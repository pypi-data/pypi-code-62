import logging

from colorlog import ColoredFormatter


# initialize logger
def initialize_logger():
    formatter = ColoredFormatter(
        '%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s '
        '%(white)s%(message)s',
        datefmt='%H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    return logger
