from crosscore.config import load_config, save_config, configdir
from crosscore import commands
from crosscore.terraform import Deployment
from crosscore.daemon import stop_daemon, start_daemon
import os.path as op
import subprocess
#
# Functions to interact with the Dask cluster from Python scripts.
# As there is only ever one cluster, no point this being a class.
#

terradir = op.join(configdir, 'terraform')
dep = Deployment(terradir)

def get_url():
    """
    Get the URL of the Dask scheduler

    Passed to Dask Client() calls.

    Returns:
        str: <hostname>:<port>
    """

    data = dep.outputs()
    return data['scheduler-url']['value']

def set_worker_type(worker_type, accelerator_type=None):
    """
    Set the worker type to be used.

    Args:
        worker_type (str): name of a valid instance type (e.g. 't2.small' 
                           or 'n1-standard-4')
        accelerator_type (str, optional): name of a valid accelerator type 
                                       (e.g. 'nvidia-tesla-t4') - for gcp only.

    Note:
        The code does not check that the names are valid!
    """

    config = load_config()
    provider = config['terraform_config']['cloud_provider']
    config['terraform_config']['worker_type'] = worker_type
    if provider == 'aws' and accelerator_type is not None:
        raise ValueError('Error: aws does not use accelerator_type')
    elif provider == 'gcp':
        if accelerator_type is None:
            config['terraform_config']['accelerator_count'] = "0"
        else:
            config['terraform_config']['accelerator_type'] = accelerator_type
            config['terraform_config']['accelerator_count'] = "1"

    save_config(config)

def set_max_workers(max_workers):
    """
    Set maximum number of worker nodes that can be launched

    Args:
        max_workers (int): maximum number of workers
    """

    config = load_config()
    config['adaptive_config']['max_workers'] = max_workers
    save_config(config)

def status():
    """
    Return the status of the cluster

    Returns:
        str: formatted status info
    """

    response = commands.status(check_daemon=False)
    return response
