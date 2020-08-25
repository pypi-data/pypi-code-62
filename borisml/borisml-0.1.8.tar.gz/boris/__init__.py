""" Deep Learning Package for Python

boris is a Python module for self-supervised active learning.

"""

try:
    import pytorch_lightning
except ImportError:
    _lightning_available = False
else:
    _lightning_available = True

try:
    import cv2
except ImportError:
    _opencv_available = False
else:
    _opencv_available = True

try:
    import prefetch_generator
except ImportError:
    _prefetch_generator_available = False
else:
    _prefetch_generator_available = True


def _cli_requires():
    return [
        'pytorch_lightning<=0.8.5',
        'opencv-python'
    ]


def is_lightning_available():
    return _lightning_available


def is_opencv_available():
    return _opencv_available


def is_prefetch_generator_available():
    return _prefetch_generator_available


if is_lightning_available():
    from ._one_liners import train_model_and_get_image_features
    from ._one_liners import train_self_supervised_model
    from ._one_liners import get_image_features

def version_compare(v0, v1):
    v0 = [int(n) for n in v0.split('.')][::-1]
    v1 = [int(n) for n in v1.split('.')][::-1]
    pairs = list(zip(v0, v1))[::-1]
    for x, y in pairs:
        if x < y:
            return -1
        if x > y:
            return 1
    return 0


def pretty_print_latest_version(latest_version, width=70):
    lines = [
        'There is a newer version of the package available.',
        'For compatability reasons, please upgrade your current version.',
        '> pip install borisml=={}'.format(latest_version),
    ]
    print('-' * width)
    for line in lines:
        print('| ' + line + (width - len(line) - 3) * " " + "|")
    print('-' * width)


from boris.api import get_latest_version
__version__ = '0.1.8'
latest_version = get_latest_version(__version__)
if latest_version is not None:
    if version_compare(__version__, latest_version) < 0:
        # local version is behind latest version
        pretty_print_latest_version(latest_version)

