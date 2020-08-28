#Copyright 2018 Infosys Ltd.
#Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at
#http://www.apache.org/licenses/LICENSE-2.0  . 
from configparser import ConfigParser
from pathlib import Path
import logging as logger

sfconnection={}
connection=''
statusmessage=''
statuscode=''
queryresult={}


def read_conf_file(conf_file_path=None):
    configparser = ConfigParser()
    if conf_file_path:
        logger.info("Using user provided snowflake configuration file")
        configparser.read(conf_file_path)
    else:
        logger.info("Using default snowflake configuration file")
        configuration_path = Path(__file__).parent / "../connections/conf.ini"
        configparser.read(configuration_path)
    return configparser
