# Copyright 2019 Splunk Inc. All rights reserved.
"""Splunk indexes.conf abstraction module"""

# Custom Libraries
from . import configuration_file


class IndexesConfigurationFile(configuration_file.ConfigurationFile):
    """Represents a [indexes.conf](http://docs.splunk.com/Documentation/Splunk/6.4.2/admin/Indexesconf#indexes.conf.example) file."""

    def __init__(self):
        configuration_file.ConfigurationFile.__init__(self)
