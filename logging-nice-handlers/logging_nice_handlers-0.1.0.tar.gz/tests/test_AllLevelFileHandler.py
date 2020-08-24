# -*- coding: utf-8 -*-

import logging

import pytest
from logging_nice_handlers import AllLevelFileHandler

def test_AllLevelFileHandler():
    LOGGER = logging.getLogger("ha-ha")
    LOGGER.setLevel(10)
    LOGGER.addHandler(AllLevelFileHandler())
    LOGGER.info("hi2")

