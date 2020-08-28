#
#  Copyright (c) 2020 Appfire Technologies, Inc.
#  All rights reserved.
#  This software is licensed under the provisions of the "Bob Swift Atlassian Add-ons EULA"
#  (https://bobswift.atlassian.net/wiki/x/WoDXBQ) as well as under the provisions of
#  the "Standard EULA" from the "Atlassian Marketplace Terms of Use" as a "Marketplace Product”
#  (http://www.atlassian.com/licensing/marketplace/termsofuse).
#  See the LICENSE file for more details.
#

import click
import subprocess
import os, shutil
import glob
from funcy import identity
import sys
import questionary
import logging
import yaml
import json


@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Verbose output")
def process(verbose):
    """
    Shallow clones the template, renames and replaces tokens with argument paramters.
    """

    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("domain_name_installer")

    appName = questionary.text("The name of your application? ").ask()
    brand = questionary.select(
        "Brand?",
        choices=[
            'bobswift',
            'wittified',
            'feed3'
        ]).ask()  # returns value of selection
    atlApp = questionary.select(
        "Atlassian App?",
        choices=[
            'confluence',
            'jira'
        ]).ask()  # returns value of selection
    brand_key = 'swift' if brand == 'bobswift' else 'wittified'
    print_func = print if verbose else identity
    print_func("Cloning the Appfire Connect App template...")

    def git(*args):
        return subprocess.check_call(['git'] + list(args))

    git("clone", "git@bitbucket.org:appfire/appfire-connect-app-template.git", "--single-branch")

    dirName = "{}-{}-connect".format(atlApp, appName)

    print_func(f'Renaming template directory root to {dirName}...')
    os.rename('appfire-connect-app-template', dirName)

    print_func(f'Switching working directory to {dirName}...')
    os.chdir(dirName)

    print_func(f'Resetting git...')
    shutil.rmtree(".git")
    git("init")

    prepare_personal_yml(logger, appName, brand)
    create_cdk_json(appName, brand)
    
    print_func(f'Updating template files...')
    for f in glob.glob("*.*"):
        with open(f, "r") as inputfile:
            newText = inputfile.read().replace('xxx', appName).replace('[atl-application]', atlApp).replace('[brand]',
                                                                                                            brand).replace('[brand_key]',brand_key)

        with open(f, "w") as outputfile:
            outputfile.write(newText)

    os.remove("README.md")
    if (os.path.isfile('README_APP.md')) :
        os.rename(r'README_APP.md',r'README.md')


if __name__ == "__main__":
    process()


def create_cdk_json(appName, brand):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("domain_name_installer")
    shell(logger, 'touch cdk.json', raise_error=True)
    # positional arguments to cdk: <appName> <stage> <domain> <appSourcePath> <brand>
    cdk_json = {
        "app": "npx ts-node ./node_modules/ac-app-dist/bin/ac-app-dist.js "
               + appName + " $STAGE $DOMAIN client/dist " + brand + "standalone "
    }

    # Serializing json
    cdk_json_object = json.dumps(cdk_json, indent=4)

    # Writing to cdk.json
    with open("cdk.json", "w") as outfile:
        outfile.write(cdk_json_object)


def prepare_personal_yml(logger, appName, brand):
    """
      prepares personal.env.yml file
    """
    shell(logger, 'touch personal.env.yml', raise_error=True)
    logger.info("personal.env.yml has been created at application root. Further modifications to "
                "domain name can be done from here")
    d = {'environment': {
        'personal': {'profile': 'default',
                     'stage': 'dev', 'domain': appName + '-dev.'+brand+'. %domain%'}}}
    with open('personal.env.yml', 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)


def shell(logger, cmdline, raise_error=False):
    """
    Run a shell command.
    :param logger:
    :param cmdline:  Shell line to be executed
    :param raise_error:
    :return: Tuple (return code, interleaved stdout and stderr output as string)
    """

    logger.debug("Running : %s" % cmdline)

    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # XXX: Support stderr interleaving
    out, err = process.communicate()

    # :E1103: *%s %r has no %r member (but some types could not be inferred)*
    # pylint: disable=E1103
    out = out.decode("utf-8")
    err = err.decode("utf-8")

    if raise_error and process.returncode != 0:
        logger.error("Command output:")
        logger.error(out + err)
        raise ShellCommandFailed("The following command did not succeed: %s" % cmdline)

    return (process.returncode, out + err)


class ShellCommandFailed(Exception):
    """ Executing a shell command failed """
