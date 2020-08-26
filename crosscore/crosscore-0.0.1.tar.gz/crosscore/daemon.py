import sys
import os
import os.path as op
import time
import logging
import daemon
import subprocess
from daemon import pidfile
from crosscore.config import load_config, save_config, configdir
from crosscore.terraform import Deployment
from distributed import Client

# adapted from:
# https://stackoverflow.com/questions/13106221/how-do-i-set-up-a-daemon-with-python-daemon
#

def update_worker_info(client, worker_info):
    """
    Get status information about all current workers
    """
    now = time.time()
    dconf = load_config()['terraform_config']
    current_workers = dconf['worker_names']
    info = client.scheduler_info()['workers']
    active_workers = [info[k]['id'] for k in info.keys()]
    r = client.retire_workers(close_workers=False, remove=False)
    retirable_workers = [info[k]['id'] for k in r]
    required_workers = [w for w in active_workers if not w in retirable_workers]
    inactive_workers = [w for w in current_workers if not w in active_workers]
    for w in list(worker_info.keys()):
        if not w in current_workers:
            worker_info.pop(w)

    for w in current_workers:
        if not w in worker_info:
            worker_info[w] = {'status': 'inactive', 
                              'idle_time': 0, 
                              'idle_start_time': now}
    for w in inactive_workers:
        worker_info[w]['status'] = 'inactive'
        worker_info[w]['idle_time'] = now - worker_info[w]['idle_start_time']
    for w in retirable_workers:
        worker_info[w]['status'] = 'retirable'
        worker_info[w]['idle_time'] = now - worker_info[w]['idle_start_time']
    for w in required_workers:
        worker_info[w]['status'] = 'required'
        worker_info[w]['idle_time'] = 0
        worker_info[w]['idle_start_time'] = now

    return worker_info

def get_n_queued_tasks(client):
    wh = client.who_has()
    queued_tasks = [w for w in wh if (wh[w] == () and not w.startswith('lambda-'))]
    return len(queued_tasks)

def get_proposed_worker_names(worker_info, n_queued_tasks):
    now = time.time()
    config = load_config()
    max_idle_time = config['adaptive_config']['max_idle_time']
    max_workers = config['adaptive_config']['max_workers']

    n_current = len(worker_info)
    n_wanted = min(max_workers, n_queued_tasks)
    current_workers = list(worker_info.keys())
    if n_wanted > n_current:
        n_to_add = n_wanted - n_current
        proposed_worker_names = ['worker-{}'.format(i) for i in 
                                  range(max_workers)]
        new_worker_names = [p for p in proposed_worker_names 
                            if not p in worker_info][:n_to_add]
        new_worker_names = current_workers + new_worker_names
    elif n_wanted < n_current:
        n_to_lose = n_current - n_wanted
        losable = [w for w in worker_info if worker_info[w]['status'] == 'inactive']
        losable += [w for w in worker_info if worker_info[w]['status'] == 'retirable' and worker_info[w]['idle_time'] > max_idle_time]
        losable = losable[:n_to_lose]
        new_worker_names = [c for c in current_workers 
                            if not c in losable]
    else:
        new_worker_names = current_workers

    return new_worker_names
    
def update_deployment(dep, new_worker_names):
    config = load_config()
    config['terraform_config']['worker_names'] = new_worker_names
    old_dconf = dep.load_config()
    dconf = config['terraform_config']
    dep.apply(dconf)
    if dep.status == 'OK':
        save_config(config)

def run(logf):
    """
    Monitor a Dask cluster and scale it according to demand.

    Args:
        logf (str): daemon log file

    """

    logger = logging.getLogger('xcore_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    try:
        logger.info('adaptive scaler started')
        config = load_config()
        client = Client(config['dask_config']['scheduler_url'], timeout=300)
        logger.info('scheduler connection established')
        dep = Deployment(op.join(configdir, 'terraform'))

        worker_info = {}
        n_queued_last = None
        poll_interval = config['adaptive_config']['poll_interval']
        logger.info('poll interval = {}s'.format(poll_interval))
        while True:
            time.sleep(poll_interval)
            config = load_config()
            poll_interval = config['adaptive_config']['poll_interval']
            worker_info = update_worker_info(client, worker_info)
            n_queued = get_n_queued_tasks(client)
            if n_queued != n_queued_last:
                logger.info('{} queued tasks'.format(n_queued))
                n_queued_last = n_queued
            new_worker_names = get_proposed_worker_names(worker_info, n_queued)
            current_workers = list(worker_info.keys())
            if set(current_workers) != set(new_worker_names):
                for w in current_workers:
                    if not w in new_worker_names:
                        logger.info('removing worker {}'.format(w))
                for w in new_worker_names:
                    if not w in current_workers:
                        logger.info('adding worker {}'.format(w))
                update_deployment(dep, new_worker_names)
                if dep.status == 'Failed':
                    logger.error('Terraform error:')
                    logger.error('Terraform stdout:\n{}'.format(dep.stdout))
                    logger.error('Terraform stderr:\n{}'.format(dep.stderr))
                    config['terraform_config'] = old_dconf
                    save_config(config)
                else:
                    logger.info('rescale succesful')


    except Exception as e:
        logger.error(str(e))
        raise
    
def start_daemon():
    """
    This launches the daemon in its context
    """

    daemondir = op.join(configdir, 'daemon')
    if not op.exists(daemondir):
        os.mkdir(daemondir)
    pidf = op.join(daemondir, 'xcore-daemon.pid')
    logf = op.join(daemondir, 'xcore-daemon.log')
    if op.exists(logf):
        os.rename(logf, logf + '.old')
    workdir = op.join(daemondir, 'work')
    if not op.exists(workdir):
        os.mkdir(workdir)
    with daemon.DaemonContext(
        working_directory=workdir,
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        ) as context:
        run(logf)

def stop_daemon():
    """
    Stop the autoscaling daemon
    """

    daemondir = op.join(configdir, 'daemon')
    pidf = op.join(daemondir, 'xcore-daemon.pid')
    if not op.exists(pidf):
        return
    with open(pidf) as f:
        pid = f.readline()
    command = 'kill {}'.format(pid)
    result = subprocess.run(command, shell=True)

def daemon_running():
    """
    Determine if the daemon is running or not.

    Returns:
        Bool: True if running, False if not.
    """

    daemondir = op.join(configdir, 'daemon')
    pidf = op.join(daemondir, 'xcore-daemon.pid')
    return op.exists(pidf)

def daemon_log():
    """
    Return the contents of the daemon log file

    Returns:
        bytes: contents of the daemon log file
    """

    daemondir = op.join(configdir, 'daemon')
    logf = op.join(daemondir, 'xcore-daemon.log')
    with open(logf) as f:
        data = f.read()
    return data

