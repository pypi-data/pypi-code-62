#!/usr/bin/python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 licence.
# See LICENSE file for details.

import os

# constants

podcast_cache_dir = ("%s/.cache/podcasthander/" % os.environ['HOME'])
daemon_data_file  = podcast_cache_dir + "daemon_data"
current_file = podcast_cache_dir + "current"
daemon_filename   = "podcasthandlerd"
default_host      = "localhost"
update_time = 3
