# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: __init__.py.py
@time: 2020/3/24 11:11

这一行开始写关于本文件的说明与解释


"""
# Make sure that leslie is running on Python 3.6.1 or later
# (to avoid running into this bug: https://bugs.python.org/issue29246)
import sys

if sys.version_info < (3, 6, 1):
    raise RuntimeError("Leslie requires Python 3.6.1 or later")

# We get a lot of these spurious warnings,
# see https://github.com/ContinuumIO/anaconda-issues/issues/6678
import warnings  # noqa

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

try:
    # On some systems this prevents the dreaded
    # ImportError: dlopen: cannot load any more object with static TLS
    import tensorflow, numpy  # noqa

except ModuleNotFoundError:
    print(
        "Using Leslie requires the python packages, "
        "tensorflow and Numpy to be installed."
    )
    raise

from leslie.version import VERSION as __version__  # noqa