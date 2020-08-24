# -*- coding: utf-8 -*-

import logging

import pytest
from logging_nice_handlers import JupyterStreamHandler

def test_JupyterStreamHandler():
    LOGGER = logging.getLogger("ha-ha")
    LOGGER.setLevel(10)
    LOGGER.addHandler(JupyterStreamHandler())
    LOGGER.warning("hi2")

