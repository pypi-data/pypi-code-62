import threading
import itertools
import subprocess
import time
import os.path as op
import os
import sys
import json
from crosscore.config import load_config, save_config, configdir

#
# This supports a simple way to manage Terraform deployments
# through Python.
#
# The deployment must be defined through a pair of files, one is a template
# for all resources ("template.tf"), the other defining values for the
# variables defined in the template ("terraform.tfvars.json")
#
# The initial contents for template.tf are provided as a suitably-formatted
# string, while the contents of terraform.tfvars.json are set and altered by
# providing a Python dict to match.
#
def _run_progress_bar(finished_event):
    chars = itertools.cycle(r'-\|/')
    while not finished_event.is_set():
        sys.stdout.write('\rWorking ' + next(chars))
        sys.stdout.flush()
        finished_event.wait(0.2)
    sys.stdout.write('Done\n')
    sys.stdout.flush()


def create(deploymentdir, template, config):
    """
    Create a terraform deployment.

    Args:
        deploymentdir (str): The directory holding the Terraform files
        template (str): a formatted Terraform template
        config (dict): Terraform template variables
    """
    if op.exists(deploymentdir):
        raise OSError('Error: this directory already exists')
    os.makedirs(deploymentdir)
    templatefile = op.join(deploymentdir, 'template.tf')
    configfile = op.join(deploymentdir, 'terraform.tfvars.json')
    with open(templatefile, 'w') as f:
        f.write(template)
    with open(configfile, 'w') as f:
        json.dump(config, f, indent=2)
    return Deployment(deploymentdir)

class Deployment(object):
    def __init__(self, deploymentdir, progress_bar=False):
        """
        Class to control a Terraform deployment of cloud resources
        
        Args:
            deploymentdir (str): location of the deployment directory
            progress_bar (bool): whether to show an interactive progress meter
        """

        self.deploymentdir = deploymentdir
        self.templatefile = op.join(deploymentdir, 'template.tf')
        self.configfile = op.join(deploymentdir, 'terraform.tfvars.json')
        self.statefile = op.join(deploymentdir, 'terraform.tfstate')
        if not op.exists(self.configfile) or not op.exists(self.templatefile):
            raise ValueError('Error - {} does not contain a valid terraform deployment'.format(self.deploymentdir))
        if not op.exists(self.statefile):
            self._spr('terraform init', progress_bar=progress_bar)

    def _spr(self, cmd, progress_bar=False, max_retries=2, retry_interval=5):

        success = False
        ntries = 0
        if progress_bar:
            finished_event = threading.Event()
            progress_bar_thread = threading.Thread(target=_run_progress_bar, args=(finished_event,))
            progress_bar_thread.start()
        while not success and ntries < max_retries:
            result = subprocess.run(cmd, shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT, 
                                cwd=self.deploymentdir)
            if result.returncode == 0:
                self.status = 'OK'
                success = True
            else:
                self.status = 'Failed'
                time.sleep(retry_interval)
            ntries += 1
        if progress_bar:
            finished_event.set()
            progress_bar_thread.join()

        self.stdout = result.stdout
        self.stderr = result.stderr

    def apply(self, config=None, progress_bar=False, max_retries=2, retry_interval=5):
        """
        Run a Terraform "apply" command, updating the cloud resources

        Args:
            config (dict, optional): update terraform.tfvars.json with 
                                     this before running "apply"
            progress_bar (bool, optional): whether to show a progress bar
            max_retries (int, optional): number of attempts to make before 
                                         giving up
            retry_interval (int, optional): interval (seconds) between retrys
        """
        if config is not None:
            with open(self.configfile, 'w') as f:
                json.dump(config, f, indent=2)
        self._spr('terraform apply -no-color -auto-approve',
                 max_retries=max_retries, retry_interval=retry_interval,
                 progress_bar=progress_bar)

    def load_config(self):
        """
        Return the current deployment configuration

        Returns:
            dict: Terraform template variables and values
        """

        with open(self.configfile) as f:
            return json.load(f)

    def save_config(self, config):
        """
        Update the  deployment configuration

        Note: this will not be implemented until "apply" is called
      
        Args:
            config (dict): Terraform template variables and values
        """
        with open(self.configfile, 'w') as f:
            json.dump(config, f, indent=2)

    def outputs(self,  max_retries=2, retry_interval=5, progress_bar=False):
        """
        Return the result of running "terraform outputs"

        Args:
            max_retries (int, optional): number of attempts to make before 
                                         giving up
            retry_interval (int, optional): interval (seconds) between retrys
            progress_bar (bool, optional): whether to show a progress bar

        Returns:
            dict
        """
        
        self._spr('terraform output -json', 
                 max_retries=max_retries, retry_interval=retry_interval,
                 progress_bar=progress_bar)
        if self.status == 'OK':
            return json.loads(self.stdout.decode())
        else:
            return None

    def destroy(self, max_retries=2, retry_interval=5, progress_bar=False):
        """
        Destroy a Terraform deployment

        Args:
            max_retries (int, optional): number of attempts to make before 
                                         giving up
            retry_interval (int, optional): interval (seconds) between retrys
            progress_bar (bool, optional): whether to show a progress bar
        """

        self._spr('terraform destroy -auto-approve -no-color', 
                 max_retries=max_retries, retry_interval=retry_interval,
                 progress_bar=progress_bar)

