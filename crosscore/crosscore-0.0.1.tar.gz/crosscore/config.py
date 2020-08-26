import os
import os.path as op
import yaml
#
# Operations on the Crosscore configuration file
#
homedir = os.getenv('HOME')
configdir = op.join(homedir, '.xcore')
if not op.exists(configdir):
    raise RuntimeError('Error: cannot find configdir')
configfile = op.join(configdir, 'config.yaml')
if not op.exists(configfile):
    raise RuntimeError('Error: cannot find config file')

def load_config():
    with open(configfile) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config

def save_config(config):
    with open(configfile, 'w') as f:
        yaml.dump(config, f)
