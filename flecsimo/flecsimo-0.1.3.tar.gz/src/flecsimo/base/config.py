"""Simple parser for json formatted config files.
Created on 29.02.2020

@author: Ralf Banning
"""

""" 
    Copyright and License Notice:

    flecsimo site control
    Copyright (C) 2020  Ralf Banning, Bernhard Lehner and Frankfurt University 
    of Applied Sciences.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import json
import pathlib

# Set default paths
libpath = (pathlib.Path(__file__).parent.parent.resolve())
db_path = libpath.joinpath("db")
conf_path = libpath.joinpath("conf")
default_conf_file = conf_path.joinpath('config.json')

def get_config(file=default_conf_file, section='DEFAULT'):
    """Get a section of a json-type config file as dictionary"""
    with open(file, mode='r') as fileh:
        config = dict(json.load(fileh))

    if section=='*':
        return config
    else:
        try:
            return config[section]
        
        # TODO: improve exception handling if sections are not defined
        except FileNotFoundError:
            print("File '", file, "' not found")
            raise
        
        except KeyError:
            print("Key '", section, "' not found")
            raise
    
def get_version(file=default_conf_file):
    """Get the current version of a config file."""
    about = get_config(file, section='About')
    return about['version']
   
def get_keys(file=default_conf_file):
    """Get all the keys of a config file."""
    conf = get_config(file, section='*')
    return conf.keys()

def get_conf_path(configfile):
    "Return the standard path to a given configfile."
    return conf_path.joinpath(configfile)

def get_db_path(dbfile):
    "Return the standard path to a given database file."
    return db_path.joinpath(dbfile)