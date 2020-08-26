from distributed import Client
from crosscore import commands, cluster, terraform
from crosscore.config import load_config, configdir, save_config
from crosscore.daemon import update_worker_info, get_proposed_worker_names, get_n_queued_tasks, update_deployment
import time
import os.path as op

def test_update_worker_info():
    c = Client(cluster.get_url())
    config = load_config()
    config['terraform_config']['worker_names'] = []
    save_config(config)
    w = update_worker_info(c, {})
    assert w == {}

def test_get_n_queued_tasks():
    c = Client(cluster.get_url())
    nq = get_n_queued_tasks(c)
    assert nq == 0
    
def test_get_proposed_worker_names():
    w = {}
    nq = 1
    c = load_config()
    c['adaptive_config']['max_workers'] = 1
    save_config(c)
    new_names = get_proposed_worker_names(w, nq)
    assert new_names == ['worker-0']
    nq = 2
    new_names = get_proposed_worker_names(w, nq)
    assert new_names == ['worker-0']
    c = load_config()
    c['adaptive_config']['max_workers'] = 2
    save_config(c)
    new_names = get_proposed_worker_names(w, nq)
    assert new_names == ['worker-0', 'worker-1']

def test_update_deployment():
    d = terraform.Deployment(op.join(configdir, 'terraform'))
    new_names = ['worker-0']
    update_deployment(d, new_names)
    assert d.status == 'OK'
    dc = d.load_config()
    assert dc['worker_names'] == new_names

def test_rescale_deployment():
    def adder(a, b):
        return a + b
    c = Client(cluster.get_url())
    r = c.submit(adder, 5, 6)
    nq = get_n_queued_tasks(c)
    assert nq == 1
    del(r)
    time.sleep(0.2)
    nq = get_n_queued_tasks(c)
    assert nq == 0


def test_update_worker_2():
    c = Client(cluster.get_url())
    config = load_config()
    config['terraform_config']['worker_names'] = ['worker-1']
    save_config(config)
    w = update_worker_info(c, {})
    assert list(w.keys()) == ['worker-1']
    assert w['worker-1']['status'] == 'inactive'
