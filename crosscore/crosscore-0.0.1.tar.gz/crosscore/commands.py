#!/usr/bin/env python
import time
import tempfile
import subprocess
import os.path as op
import os
import yaml
import json
from . import terraform
from .daemon import daemon_running, stop_daemon, start_daemon
import logging
from .config import load_config, save_config, configdir
from .aws import templates
from distributed import Client
import warnings

logger = logging.getLogger('xcore_daemon')
config = load_config()
deployment = terraform.Deployment(op.join(configdir, 'terraform'))

def status(check_daemon=True):
    """
    Report the status of the crosscore cluster

    Returns:
        str: formatted status information
    """

    response = ''
    if check_daemon:
        if not daemon_running():
            response = 'Warning: the crosscore daemon is not running\n'
            return response
    config = load_config()
    scheduler_url = config['dask_config']['scheduler_url']
    worker_type = config['terraform_config']['worker_type']
    provider = config['terraform_config']['cloud_provider']
    if provider == "gcp":
        if config['terraform_config']['accelerator_count'] != "0":
            worker_type += '+' + config['terraform_config']['accelerator_type']
    if scheduler_url is None:
        response += 'Warning: there is no crosscore cluster running\n'
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                client = Client(scheduler_url)
            except IOError:
                response += 'No response from scheduler - may still be booting up?\n'
                return response
        worker_info = client.scheduler_info()['workers']
        all_worker_info = {}
        for w, data in worker_info.items():
            all_worker_info[data['id']] = 'running  {cpu:5.1f}  {ready:6d}  {executing:10d} {in_memory:10d}'.format(**data['metrics'])
        workers = config['terraform_config']['worker_names']
        for w in workers:
            if not w in all_worker_info:
                all_worker_info[w] = 'launching'
        if len(workers) == 0:
            response += 'There are no workers running\n'
        else:
            response += ' worker type: {}\n'.format(worker_type)
            response += ' name     state     cpu  queued   executing  completed\n'
            for w in workers:
                response += '{:6s} {}\n'.format(w, all_worker_info[w])
    return response

def shutdown():
    """
    Terminate the crosscore cluster, deleting all cloud resources

    """

    if not daemon_running():
        print('Warning: the crosscore daemon is not running')

    config = load_config()
    print('Stopping daemon...')
    stop_daemon()
    print('Deleting cloud infrastructure...')
    deployment.destroy(progress_bar=True)
    if deployment.status == 'OK':
        config['dask_config']['scheduler_url'] = None
        save_config(config)
        print('All done without errors.')
    else:
        print(deployment.stdout)
        print(deployment.stderr)
        print('Warning: There were errors in the clean-up and some cloud resources may remain.')

def start(restart=False):
    """
    Start the crosscore cluster - launch the scheduler.

    Args:
        restart (Bool): If True this is a restart, not first start.
    """
    if restart:
        print('Recreating cloud infrastructure...')
        stop_daemon()
    else:
        print('Creating cloud infrastructure...')
    config = load_config()
    deployment.apply(config['terraform_config'], progress_bar=True)
    if deployment.status == "OK":
        data = deployment.outputs()
        config['dask_config']['scheduler_url'] = data['scheduler-url']['value']
        save_config(config)
        if restart:
            print('Restarting daemon...')
        else:
            print('Starting daemon...')
        start_daemon()
    else:
        print(deployment.stdout)
        print(deployment.stderr)
        if restart:
            print('Warning: There were errors restarting and some cloud resources may be missing.')
        else:
            print('Warning: There were errors starting and some cloud resources may be missing.')
    
