from distributed import Client
from crosscore import commands, cluster, terraform
from crosscore.config import load_config, configdir, save_config
import time
import os.path as op

def test_creation(tmp_path):
    depdir = tmp_path / 'sub'
    d = terraform.create(depdir, 'template', 'varfile')
    assert isinstance(d, terraform.Deployment)

def test_save_load_config(tmp_path):
    depdir = tmp_path / 'sub'
    d = terraform.create(depdir, 'template', 'varfile')
    config = {'variable': 'value'}
    d.save_config(config)
    config2 = d.load_config()
    assert config2 == config
    
def test_apply(tmp_path):
    depdir = tmp_path / 'sub'
    d = terraform.create(depdir, 'template', 'varfile')
    d.apply()
    assert d.status == 'OK'

def test_outputs(tmp_path):
    depdir = tmp_path / 'sub'
    d = terraform.create(depdir, 'template', 'varfile')
    outputs = d.outputs()
    assert outputs == {'scheduler-url': {'value': '127.0.0.1:8786'}}

