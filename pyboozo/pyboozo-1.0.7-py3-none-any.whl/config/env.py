## Copyright (c) 2020 mangalbhaskar.
"""Environment configuration variables and setup.

References:
* https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
"""
__author_ = 'mangalbhaskar'

__all_ = [
  'EnvCfgo'
]

import logging
import logging.config
import os
import re
import sys

from boozo.config._log_ import logcfg
log = logging.getLogger('__main__.'+__name__)
logging.config.dictConfig(logcfg)

from boozo.utils import cast
from boozo.utils import common

this = sys.modules[__name__]
this_dir = os.path.dirname(__file__)
current_dirpath = os.getcwd()


class EnvCfgo(object):
  """Configuration"""
  _ROOT = None
  _NAME = 'boozo'
  _PREFIX = '_BZO'
  _IS_TIMESTAMP_DATA_DIR = False

  _VMHOME = None
  _PYVENV_PATH = None

  _APACHE_HOME = None
  _WSGIPythonHome = None
  _WSGIPythonPath = None
  
  _PYENVVAR = None

  _CONFIG_ROOT = None
  _DATA_ROOT = None
  _MOBILE_ROOT = None

  _WEB_APP = None
  _WEB_APP_LOGS = None
  _VAR = None
  
  _HOME = None
  _CONFIG = None
  _DATA_HOME = None
  _MOBILE_HOME = None

  _DIR_PATH = None
  _DATA_DIR_PATH = None
  _MOBILE_DIR_PATH = None

  _ALIAS = {
    '_HOME'
    ,'_NAME'
    ,'_SCRIPTS'
    ,'_APPS'
    ,'_COMMON'
    ,'_CFG'
    ,'_CONFIG'
    ,'_DATA_HOME'
    ,'_DIST'
    ,'_EXTERNAL'
    ,'_LOGS'
    ,'_TMP'
    ,'_DOCS'
    ,'_REPORTS'
    ,'_KBANK'
    ,'_MNT'
    ,'_MOBILE'
    ,'_DOWNLOADS'
  }
  _DIR = (
    'apps'
    ,'common'
    ,'dist'
    ,'docs'
    ,'plugins'
    ,'practice'
    ,'scripts'
    ,'tests'
    ,'www'
  )
  _DATA_DIR = (
    'ant'
    ,'aid'
    ,'aid/tfrecords'
    ,'auth'
    ,'cfg'
    ,'cloud'
    ,'databases'
    ,'databases/mongodb'
    ,'databases/mongodb/db'
    ,'databases/mongodb/logs'
    ,'databases/mongodb/key'
    ,'databases/mongodb/configdb'
    ,'docker'
    ,'downloads'
    ,'external'
    ,'kbank'
    ,'logs'
    ,'logs/www'
    ,'mobile'
    ,'mnt'
    ,'npm-packages'
    ,'public'
    ,'public_html'
    ,'release'
    ,'release/keras'
    ,'release/torch'
    ,'reports'
    ,'samples'
    ,'_site'
    ,'team'
    ,'team/images'
    ,'tools'
    ,'tmp'
    ,'uploads'
    ,'workspaces'
  )
  _MOBILE_DIR = (
    'android'
    ,'android/apps'
    ,'android/dist'
    ,'android/external'
    ,'android/plugins'
    ,'android/sdk'
  )
  _PATH = {
    '_APPS':'apps'
    ,'_LSCRIPTS':'scripts/lscripts'
    ,'_PRACTICE':'practice'
    ,'_PLUGINS':'plugins'
    ,'_COMMON':'common'
    ,'_DOCS':'docs'
    ,'_DIST':'dist'
    ,'_SCRIPTS':'scripts'
    ,'_WWW_HOME':'www'
  }
  _DATA_PATH = {
    '_AUTH':'auth'
    ,'_CFG':'cfg'
    ,'_DATABASE':'database'
    ,'_DOWNLOADS':'downloads'
    ,'_KBANK':'kbank'
    ,'_LOGS':'logs'
    ,'_MNT':'mnt'
    ,'_NPM':'npm-packages'
    ,'_RELEASE':'release'
    ,'_REPORTS':'reports'
    ,'_SAMPLES':'samples'
    ,'_SITE':'_site'
    ,'_TFRECORDS':'tfrecords'
    ,'_TOOLS':'tools'
    ,'_TMP':'tmp'
    ,'_WWW_LOGS':'logs/www'
    ,'_WWW_UPLOADS':'uploads'
    ,'_WORKSPACE':'workspaces'
    ,'_WWW':'public_html'
    ,'_EXTERNAL':'external'
  }
  _MOBILE_PATH = {
    '_ANDROID_HOME':'android/sdk'
  }

  ## dynamically created
  _LINK = {}
  _ENVCFG = None

  def __init__(self, options=dict()):
    _opts = [
      '_NAME'
      ,'_ROOT'
      ,'_PREFIX'
      ,'_IS_TIMESTAMP_DATA_DIR'
      ,'_VMHOME'
      ,'_WSGIPythonHome'
      ,'_APACHE_HOME'
    ]
    log.debug("options: {}".format(options))

    if options and len(options) > 0:
      for k,v in options.items():
        if k in _opts and v is not None and v:
          v = self.app_prefix(v) if k == '_PREFIX' else v
          v = self.app_name(v) if k == '_NAME' else v
          v = self.app_root(v) if k == '_ROOT' else v
          log.debug('k:{}, v:{}'.format(k,v))
          setattr(self, k, v)

    self._ROOT =  self._ROOT if self._ROOT else os.path.join(current_dirpath, "{}-{}".format(os.path.basename(this_dir), 'hub'))
    self._NAME = self._NAME
    self._HOME =  os.path.join(self._ROOT, "{}".format(self._NAME))
    ##
    self._IS_TIMESTAMP_DATA_DIR = cast.to_bool(self._IS_TIMESTAMP_DATA_DIR) if self._IS_TIMESTAMP_DATA_DIR else False
    self._WSGIPythonPath = os.path.join(self._WSGIPythonHome,'bin') if self._WSGIPythonHome else None
    self._APACHE_HOME = self._APACHE_HOME if self._APACHE_HOME else os.path.join(self._ROOT, 'www')
    ##
    self._VMHOME = os.path.join(self._ROOT, 'virtualmachines')
    self._PYVENV_PATH = os.path.join(self._VMHOME,'virtualenvs')
    self._PYVENV_HOME = os.path.join(self._HOME, 'virtualenvs')
    ##
    self._CONFIG = os.path.join(self._HOME, 'config')
    self._MOBILE_HOME = os.path.join(self._HOME, 'mobile')
    self._CONFIG_ROOT = os.path.join(self._ROOT, "{}-{}".format(self._HOME, 'config'))
    self._DATA_HOME = os.path.join(self._HOME, 'data')
    self._LOGS_HOME = os.path.join(self._HOME, 'logs')
    self._TMP_HOME = os.path.join(self._HOME, 'tmp')

    self._DATA_ROOT = os.path.join(self._ROOT, "{}-{}".format(self._HOME, 'dat'))
    self._MOBILE_ROOT = os.path.join(self._ROOT, "{}-{}".format(self._HOME, 'mobile'))
    ## core directories
    self._PATH = { k: os.path.join(self._HOME, v) for k,v in self._PATH.items() }
    self._DIR_PATH = [os.path.join(self._HOME, d) for d in self._DIR]
    ## Data directories
    self._DATA_PATH = { k: os.path.join(self._DATA_HOME, v) for k,v in self._DATA_PATH.items() }
    self._DATA_DIR_PATH = [os.path.join(self._DATA_ROOT, d) for d in self._DATA_DIR]
    ## Mobile directories
    self._MOBILE_PATH = { k: os.path.join(self._MOBILE_HOME, v) for k,v in self._MOBILE_PATH.items() }
    self._MOBILE_DIR_PATH = [os.path.join(self._MOBILE_ROOT, d) for d in self._MOBILE_DIR]
    ## www
    self._APACHE_HOME = self._DATA_PATH['_WWW']
    ## Link dictionary
    self._LINK[self._CONFIG] = self._CONFIG_ROOT
    self._LINK[self._DATA_HOME] = self._DATA_ROOT
    self._LINK[self._MOBILE_HOME] = self._MOBILE_ROOT
    self._LINK[self._PYVENV_HOME] = self._PYVENV_PATH
    self._LINK[self._LOGS_HOME] = self._DATA_PATH['_LOGS']
    self._LINK[self._TMP_HOME] = self._DATA_PATH['_TMP']
    ## alias
    self._ALIAS = { self.get(a): '"cd ${'+self.get(a)+'}"' for a in self._ALIAS }
    ## environment configurations
    self._VAR = ":".join([
      self.get(k) for k,v in self.__dict__.items() \
        if k not in ['_LINK', '_ALIAS', '_PREFIX']
    ])
    self._ENVCFG = self.get_envcfg()

  def _fix_prefix(self, d):
    """Caution: recursive function to change the prefix for the keys in the dictionary variables."""
    d_mod = { self.get(k):d[k] if not dict == type(d[k]) else self._fix_prefix(d[k]) for k in d.keys() }
    return d_mod

  def app_root(self, s=''):
    """app root directory checks."""
    log.debug("app root directory checks.")
    _root = re.sub('[^A-Za-z\/-]+', '', s) if s else self._ROOT
    log.debug("_root: {}".format(_root))
    if _root == '/':
      raise IOError('Provide the valid application root directory. System Root ("/") cannot be used directly')
    return _root

  def app_name(self, s=''):
    """app prefix char should limit to 7 char maximum to avoid too long names."""
    log.debug("app prefix char should limit to 7 char maximum to avoid too long names.")
    return re.sub('[^A-Za-z]+', '', s.lower())[0:7] if s else self._NAME

  def app_prefix(self, s=''):
    """app prefix char should limit to 3 char maximum to avoid too long names."""
    log.debug("app prefix char should limit to 3 char maximum to avoid too long names.")
    return re.sub('[^A-Za-z]+', '', s.upper())[0:3] if s else self._PREFIX

  def get(self, a):
    return self._PREFIX+'_'+a.upper().split('__')[-1]

  def get_kwargs(self):
    kwargs = {}
    for attr, v in self.__dict__.items():
      # if attr in ['_LINK', '_ALIAS']:
      #   continue
      kwargs[attr] = v
    return kwargs

  def get_envcfg(self):
    """Create the environment config variable based on the required prefix."""
    _envcfg = {}
    for attr, v in self.__dict__.items():
      if attr in ['_LINK', '_ALIAS']:
        continue
      log.debug("attr: {}".format(attr))
      v = self._fix_prefix(v) if type(v) == dict else v
      prefix = self.get(attr)
      _envcfg[prefix] = v
    return _envcfg
