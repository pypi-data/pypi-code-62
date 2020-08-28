#
#  Copyright (c) 2020 Appfire Technologies, Inc.
#  All rights reserved.
#  This software is licensed under the provisions of the "Bob Swift Atlassian Add-ons EULA"
#  (https://bobswift.atlassian.net/wiki/x/WoDXBQ) as well as under the provisions of
#  the "Standard EULA" from the "Atlassian Marketplace Terms of Use" as a "Marketplace Product”
#  (http://www.atlassian.com/licensing/marketplace/termsofuse).
#  See the LICENSE file for more details.
#

import json
import coloredlogs,logging
import subprocess
import sys
import click
import yaml
import os


@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Verbose output")
@click.option('--profile', '-p', help="AWS profile as the default environment")
@click.option('--env', '-e', help="standalone, dts or prod", default="standalone")
@click.option('--stack', '-s', help="CDK stack to deploy", default="app")
@click.option('--stage', '-stage', help="dev, test, stage or prod", default="dev")
@click.option('--app-suffix', '-as', help="blue or green", default="blue")
@click.option('--build','-b',help="True or False",default=True)
@click.option('--api-domain','-api-domain',help="API domain for Core Services(common.appfire.app or dts.common.appfire.app or services.custom-domain)")
@click.option('--api-stage','-api-stage',help="API stage for Core Services(prod or snapshot or stage)")
@click.option('--require-approval','-require-approval',help="never or any-change or broadening",default="never")
@click.argument('command')
def process(verbose, command, profile, env, stage, stack, app_suffix, build, api_domain, api_stage, require_approval):
    """
    gathers information related to deployment and deploys the CDK stack
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("ac_app_deploy")
    coloredlogs.install(level='DEBUG',logger=logger)
    logger.debug("checking environment " + env)
    if env == 'standalone':
        personal_env_settings = None
        try:
            with open("./personal.env.yml", 'r') as stream:
                    personal_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.info(exc)
        except IOError:
            logger.info("personal.env.yml not found!")
        aws_profile = profile if profile else personal_env_settings['environment']['personal']['profile']
        domain = personal_env_settings['environment']['personal']['domain']
        log_info(logger, aws_profile, domain, env)
        ### Check if CDK_DEPLOY_ACCOUNT and CDK_DEPLOY_REGION exist in personal.env.yml
        if personal_env_settings['environment']['personal']['CDK_DEPLOY_ACCOUNT'] and personal_env_settings['environment']['personal']['CDK_DEPLOY_REGION'] :
            #### Setting env varibale CDK_DEPLOY_ACCOUNT and CDK_DEPLOY_REGION for standalone deployment
            logger.info("Setting up Env variables : CDK_DEPLOY_ACCOUNT {}, CDK_DEPLOY_REGION {}".format(personal_env_settings['environment']['personal']['CDK_DEPLOY_ACCOUNT'],personal_env_settings['environment']['personal']['CDK_DEPLOY_REGION']))
            os.environ["CDK_DEPLOY_ACCOUNT"] = str(personal_env_settings['environment']['personal']['CDK_DEPLOY_ACCOUNT'])
            os.environ["CDK_DEPLOY_REGION"] = personal_env_settings['environment']['personal']['CDK_DEPLOY_REGION']
        else :
            logger.info("CDK_DEPLOY_ACCOUNT and CDK_DEPLOY_REGION is not found in personal.env.yml.")
        #### Set API_DOMAIN, API_STAGE, API_PATH as env variable
        api_domain = api_domain if api_domain else personal_env_settings['environment']['personal']['api_domain']
        api_stage =  api_stage if api_stage else personal_env_settings['environment']['personal']['api_stage']
        api_path = api_domain+"/"+api_stage
        logger.info("Setting up Env variables : API_DOMAIN {}, API_STAGE {}, API_PATH {}".format(api_domain, api_stage, api_path))
        os.environ["API_DOMAIN"] = api_domain
        os.environ["API_STAGE"] = api_stage
        os.environ["API_PATH"] = api_path
    elif env == 'dts':
        dts_env_settings = None
        try:
            with open("./env.yml", 'r') as stream:
                dts_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
                logger.info(exc)
        except IOError:
                logger.info("env.yml not found!")
        aws_profile = profile if profile else dts_env_settings['environment'][env][stage]['profile']
        domain = dts_env_settings['environment'][env][stage]['domain']
        log_info(logger, aws_profile, domain, env)
        #### Set API_DOMAIN, API_STAGE, API_PATH as env variable
        if api_domain :
            api_domain = api_domain
        elif 'api_domain' in dts_env_settings['environment'][env][stage].keys() :
            api_domain =  dts_env_settings['environment'][env][stage]['api_domain']
        elif 'api_domain' in dts_env_settings['environment'][env]["default"].keys() :
            api_domain =  dts_env_settings['environment'][env]["default"]['api_domain']
        else :
            api_domain = api_domain

        if api_stage :
            api_stage = api_stage
        elif 'api_stage' in dts_env_settings['environment'][env][stage].keys() :
            api_stage =  dts_env_settings['environment'][env][stage]['api_stage']
        elif 'api_stage' in dts_env_settings['environment'][env]["default"].keys() :
            api_stage =  dts_env_settings['environment'][env]["default"]['api_stage']
        else :
            api_stage = api_stage

        api_path = api_domain+"/"+api_stage
        logger.info("Setting up Env variables : API_DOMAIN {}, API_STAGE {}, API_PATH {}".format(api_domain, api_stage, api_path))
        os.environ["API_DOMAIN"] = api_domain
        os.environ["API_STAGE"] = api_stage
        os.environ["API_PATH"] = api_path
    else:
        prod_env_settings = None
        try:
            with open("./env.yml", 'r') as stream:
                prod_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.info(exc)
        except IOError:
            logger.info("env.yml not found!")
        aws_profile = profile if profile else prod_env_settings['environment'][env]['profile']
        domain = prod_env_settings['environment'][env]['domain']
        log_info(logger, aws_profile, domain, env)
        #### Set API_DOMAIN, API_STAGE, API_PATH as env variable
        api_domain = api_domain if api_domain else prod_env_settings['environment'][env]['api_domain']
        api_stage = ""
        api_path = api_domain
        logger.info("Setting up Env variables : API_DOMAIN {}, API_STAGE {}, API_PATH {}".format(api_domain, api_stage, api_path))
        os.environ["API_DOMAIN"] = api_domain
        os.environ["API_STAGE"] = api_stage
        os.environ["API_PATH"] = api_path
    
    ### Setting Envrionment Variables
    logger.info("Setting up environment variables : AWS_APP_DOMAIN, AWS_PROFILE")
    os.environ["AWS_APP_DOMAIN"] = domain
    os.environ["AWS_PROFILE"] = aws_profile

    if command.lower() == 'bootstrap':
        shell(logger, "cdk bootstrap", raise_error=True)
    elif command.lower() == 'build':
        logger.debug("------------ Running Build --------------------")
        shell(logger, "rm -rf client && npm run build",raise_error=True)
    elif command.lower() == 'deploy':
        # DTS GREEN: xxx-green-dev.dts-bobswift.appfire.app
        # DTS BLUE: xxx-dev.dts-bobswift.appfire.app
        # STANDALONE: xxx-dev.bobswift.lavadukanam.com
        # PROD: markdown.bobswift.appfire.app

        app_domain = domain.split(".")[2] + "." + domain.split(".")[3] if env == 'standalone' else "appfire.app"
        app_name = domain.split(".")[0].split("-")[0]
        #brand = domain.split(".")[1] if env != 'standalone' else "bobswift"
        brand = domain.split(".")[1].replace('dts-','') if env == 'dts' else domain.split(".")[1]
        logger.info("brand : "+ brand)
        #print(brand)
        #print(domain.split("."))
        app_suffix = 'green' if app_suffix == 'green' else ''
        
        ## Run build by default. Escape if false
        if build == True :
            logger.debug("------------ Running Build --------------------")
            shell(logger, "rm -rf client && npm run build",raise_error=True)
        
        #generate_base_url(logger, "web/static/atlassian-connect.json", app_suffix, domain, env)
        #generate_base_url(logger, "atlassian-connect.json", app_suffix, domain, env)
        logger.debug("overriding cdk.json with supplied arguments")
        generate_cdk_json(logger, app_suffix, app_domain, env, stack, stage, brand, app_name)
        if stack == 'core':
            deploy_core(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile)
        elif stack == 'biz-service':
            deploy_biz_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile)
        elif stack == 'app-service':
            deploy_app_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile)
        elif stack == 'module-service':
            deploy_module_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile)
        else:
            shell(logger, "cdk deploy '*' --require-approval "+ require_approval +" --profile " + aws_profile, raise_error=True)
    elif command == 'diff':
        shell(logger, "cdk diff --profile " + aws_profile, raise_error=True)
    elif command == 'synth':
        shell(logger, "cdk synth --profile " + aws_profile, raise_error=True)
    elif command == 'destroy':
        shell(logger, "cdk destroy " + stack + "--profile " + aws_profile, raise_error=True)
    else:
        shell(logger, "cdk list --profile " + aws_profile, raise_error=True)


def deploy_core(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile):
    if deploy_biz_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile) :
        if deploy_app_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile) :
            if deploy_module_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile):
                print('Core services deployed successfully.')

def deploy_biz_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile):
    if (not os.path.isfile('./node_modules/ac-biz-services/bin/ac-biz-services.js')):
        logger.info('ac-biz-services dependency is not installed. Installing latest ac-biz-services.')
        shell(logger,"npm install ac-biz-services --save-dev",raise_error=True)

    shell(logger, "cdk deploy '*' --app 'npx ts-node ./node_modules/ac-biz-services/bin/ac-biz-services.js " + env + " " + stage + "'" +
                  " --require-approval never --profile " + aws_profile, raise_error=True)
    return True

def deploy_app_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile):
    if (not os.path.isfile('./node_modules/ac-app-services/bin/ac-app-services.js')):
        logger.info('ac-app-services dependency is not installed. Installing latest ac-app-services.')
        shell(logger,"npm install ac-app-services --save-dev",raise_error=True)
    
    ## install dependencies for app services
    logger.info("Installing dependencies for App Services")
    shell(logger,"cd ./node_modules/ac-app-services/lib/lifecycle/construct/resources/lifecycle-node-layer/nodejs && npm install && cd -",raise_error=True)
    shell(logger,"cd ./node_modules/ac-app-services/lib/webhook-router/construct/resources && npm install && cd - ",raise_error=True)
    shell(logger,"cd ./node_modules/ac-app-services/lib/waf-services/construct/resources/waf-shield && pip3 install requests -t ./ && cd -",raise_error=True)

    shell(logger, "cdk deploy '*' --app 'npx ts-node ./node_modules/ac-app-services/bin/ac-app-services.js " + env 
                                + " " + app_domain + " " + brand + "'" +
                  " --require-approval never --profile " + aws_profile, raise_error=True)
    return True

def deploy_module_services(logger,app_name,stage,app_domain,brand,env,app_suffix,aws_profile):
    if (not os.path.isfile('./node_modules/ac-module-services/bin/ac-module-services.js')):
        logger.info('ac-module-services dependency is not installed. Installing latest ac-module-services.')
        shell(logger,"npm install ac-module-services --save-dev",raise_error=True)
    
    ## install dependencies for module services
    logger.info("Installing dependencies for Module Services")
    shell(logger,"cd ./node_modules/ac-module-services/lib/API/resources/modules-lambda-layer/nodejs && npm install && cd -", raise_error=True)
    shell(logger,"cd ./node_modules/ac-module-services/lib/jwt/construct/resources/jwt-auth-node-layer/nodejs && npm install && cd -",raise_error=True)

    ## check if automation resources do not exist , then create 
    if not os.path.isfile('./node_modules/ac-module-services/lib/API/resources/automation-lambda/build/libs/automation-lambda.jar') or not os.path.isfile('./node_modules/ac-module-services/lib/API/resources/automation-lambda/build/distributions/lambda-layer-dependencies.zip'):
        shell(logger,"cd ./node_modules/ac-module-services/lib/API/resources/automation-lambda && ./gradlew clean build --refresh-dependencies && cd - ",raise_error=True)

    ## Deploying ac-module-services
    shell(logger, "cdk deploy '*' --app 'npx ts-node ./node_modules/ac-module-services/bin/ac-module-services.js " + env + " " + app_domain + "'" +
                  " --require-approval never --profile " + aws_profile, raise_error=True)
    return True

def generate_cdk_json(logger, app_suffix, app_domain, env, stack, stage, brand, app_name):
    '''dynamically prepare cdk.json based on command line arguments'''
    
    try:
        with open('cdk.json', 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                if item == 'app':
                    json_data[
                        item] = "npx ts-node ./node_modules/ac-app-dist/bin/ac-app-dist.js " + app_name + " " + stage \
                                + " " + app_domain + " client/dist " + brand + " " + env + " false " + app_suffix
        with open('cdk.json', 'w') as file:
            json.dump(json_data, file, indent=2)
    except IOError:
        shell(logger, "cdk.json not found!")


def generate_base_url(logger, path, app_suffix, domain, env):
    '''generate baseurl in atlassian-connect descriptor'''
    
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                if item == 'baseUrl':
                    if env == 'dts':
                        app_name = domain.split(".")[0].split("-")[0]
                        env_stage = domain.split(".")[0].split("-")[1]
                        domain = domain if app_suffix != 'green' else app_name + "-green-" + env_stage + "." + \
                                                                      domain.split(".")[1] + "." + \
                                                                      domain.split(".")[2] + "." + \
                                                                      domain.split(".")[3]
                    if env == 'prod':
                        app_name = domain.split(".")[0]
                        domain = domain if app_suffix != 'green' else app_name + "-green." + \
                                                                      domain.split(".")[1] + "." + \
                                                                      domain.split(".")[2] + "." + \
                                                                      domain.split(".")[3]
                    
                    json_data[item] = "https://" + domain
                if item == 'links':
                    json_data['links']['self'] = "https://" + domain + "/atlassian-connect.json"
        
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
    except IOError:
        shell(logger, path + " not found!")


def log_info(logger, aws_profile, domain, env):
    logger.info(f'Environment: {env}')
    logger.info(f'AWS Profile: {aws_profile}')
    logger.info(f'Domain: {domain}')

def shell(logger, cmd, raise_error=False):
    """
    Run a shell command.
    :param logger:
    :param cmd:  Shell line to be executed
    :param raise_error:
    :return: Tuple (return code, interleaved stdout and stderr output as string)
    """
    
    logger.debug("Running : %s" % cmd)
    process = subprocess.run(
        cmd,
        check=True,
        shell=True
    )
    if raise_error and process.returncode != 0:
        logger.error("Command output:")
        raise ShellCommandFailed("The following command did not succeed: %s" % cmd)
    
    return (process.returncode)


class ShellCommandFailed(Exception):
    """ Executing a shell command failed """


if __name__ == "__main__":
    process()
