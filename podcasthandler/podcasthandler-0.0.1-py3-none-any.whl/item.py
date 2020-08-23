#!/usr/bin/python3

# PODCAST HANDLER by Claudio Barca (Copyright 2020 Claudio Barca)
# This software is distributed under GPL v. 3 licence.
# See LICENSE file for details.

import os
import hashlib

class Item:
    def __init__(self,url):
        podcast_cache_dir = ("%s/.cache/podcast-hander/" % os.environ['HOME'])
        self.url = url
        self.hash = self.get_hash_string()
        self.cache_file = podcast_cache_dir + self.hash    # save the position of a podcast
        self.current_file = podcast_cache_dir + "current"  # save the current podcast url

        # Create cache directory & all intermediate directories if don't exists
        if not os.path.exists(podcast_cache_dir):
            os.makedirs(podcast_cache_dir)
            print("Directory " , podcast_cache_dir,  " Created ")

    def db_get_position(self):
        try:
            file = open(self.cache_file,'r') 
            position = int(file.readlines()[0])
            return position
        except:
            return 0

    def db_set_position(self,position):
        file = open(self.cache_file,'w') 
        file.write(position)
        file.close() 

    def db_set_current(self):   # save the current podcast url
        file = open(self.current_file,'w') 
        file.write(self.url)
        file.close() 

    def db_delete_cache_file():
        try:
            os.remove(self.cache_file)
        except:
            print('No cache file')

    # the cache filename is a sha256 hash of the url text
    def get_hash_string(self):
        hash = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        return hash


