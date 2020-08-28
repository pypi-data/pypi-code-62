from ipytv.db import add_channel, update_channel, print_channels, \
    total_channels, get_channels
from os.path import join, dirname


class IPTV:
    def __init__(self, lang="en", db_path=None):
        self.db_path = db_path or join(dirname(__file__), "res",
                                       "channels.jsondb")
        self.lang = lang

    def add_channel(self, channel):
        add_channel(channel, self.db_path)

    def update_channel(self, channel):
        update_channel(channel, self.db_path, self.lang)

    def print_channels(self):
        print_channels(self.db_path)

    @property
    def channels(self):
        return list(set(get_channels(self.db_path)))

    @property
    def channel_names(self):
        return list(set([ch.name for ch in self.channels]))

    @property
    def total_channels(self):
        return total_channels(self.db_path)


