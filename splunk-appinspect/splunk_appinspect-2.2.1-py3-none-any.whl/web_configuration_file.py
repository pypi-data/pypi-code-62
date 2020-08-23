# Copyright 2019 Splunk Inc. All rights reserved.
"""Splunk web.conf abstraction module"""

# Custom Libraries
from . import configuration_file


class WebConfigurationFile(configuration_file.ConfigurationFile):
    """Represents a [web.conf](http://docs.splunk.com/Documentation/Splunk/latest/Admin/Webconf) file."""

    def __init__(self):
        configuration_file.ConfigurationFile.__init__(self)
