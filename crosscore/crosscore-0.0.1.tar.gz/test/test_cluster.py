from distributed import Client
from crosscore import commands, cluster, terraform
from crosscore.config import load_config, configdir, save_config
import time
import os.path as op

def test_status():
    config = load_config()
    config['terraform_config']['worker_names'] = []
    save_config(config)
    status = cluster.status()
    assert status == 'There are no workers running\n'

def test_set_max_workers():
    cluster.set_max_workers(1)
    conf = load_config()
    assert conf['adaptive_config']['max_workers'] == 1
    cluster.set_max_workers(6)
    conf = load_config()
    assert conf['adaptive_config']['max_workers'] == 6

def test_worker_type():
    cluster.set_worker_type('test-instance-type')
    conf = load_config()
    assert conf['terraform_config']['worker_type'] == 'test-instance-type'
    if conf['terraform_config']['cloud_provider'] == 'gcp':
        assert conf['terraform_config']['accelerator_count'] == '0'
        cluster.set_worker_type('gpu-instance-type', accelerator_type='test-accelerator-type')
        conf = load_config()
        assert conf['terraform_config']['worker_type'] == 'gpu-instance-type'
        assert conf['terraform_config']['accelerator_count'] == '1'

