from pyfiglet import Figlet
import click
import time
import os
import sys
import json
import urllib
import urllib3
from urllib.parse import urljoin

from vessel.steps import VaultInitStep, VaultSaveSecretsStep, GenerateKeysStep, \
  RegisterStep, VaultUnsealStep, GenerateYamlStep, DeployAgentStep, DeploySentinelStep
from vessel.pipeline import Pipeline, Payload
from vessel.logging import logger
from vessel.version import VERSION, LATEST_AGENT, LATEST_SENTINEL
from vessel.utilities import sanitizeClusterName
import kubernetes
from kubernetes.client.rest import ApiException



def start(msg):
  click.echo(f"\n> {msg}...")

def end(msg):
  click.echo(f"[*] {msg}")

def prompt(msg, tag, **kwargs):
  return click.prompt(msg, type=str, **kwargs)

@click.group( invoke_without_command=True)
@click.option('--debug', is_flag=True, default=False, help="output debug log [False]")
@click.option('--version', is_flag=True, default=False,  help="Show version and exits")
@click.pass_context
def main(ctx, debug, version):
  """
  Vessel cli tool 
  """
  if version:
    print(f"Vessel cli tool: {VERSION}")
    sys.exit()

  if ctx.invoked_subcommand is None:
    print(ctx.get_help())
    sys.exit()

  click.clear()
  f = Figlet(font='standard')
  click.echo(f.renderText('Vessel cli tool'))
  ctx.ensure_object(dict)
  ctx.obj['DEBUG'] = debug

  if debug:
    logger.setLevel("DEBUG")
  
  # Init directories
  if not os.path.exists(os.path.expanduser("~/.daas")):
      os.mkdir( os.path.expanduser("~/.daas"))

@main.command()
@click.pass_context
@click.option('--vault', default='http://vault.local', help='Vault endpoint [http://vault.local]')
def init(ctx, vault):
  """
  Init vault
  """
  payload = Payload()
  pipeline = Pipeline(start_fn=start, end_fn=end, prompt_fn=prompt)
  pipeline.add(VaultInitStep(vault))
  try:
    # Run pipeline
    payload = pipeline.run(payload)    
  except Exception as e:
    logger.error(e)
    if ctx.obj['DEBUG']:
      raise e

@main.command()
@click.pass_context
@click.option('--vault', default='http://vault.local', help='Vault endpoint [http://vault.local]')
def unseal(ctx, vault):
  """
  Unseal vault
  """
  payload = Payload()
  pipeline = Pipeline(start_fn=start, end_fn=end, prompt_fn=prompt)
  pipeline.add(VaultUnsealStep(vault))
  try:
    # Run pipeline
    payload = pipeline.run(payload)    
  except Exception as e:
    logger.error(e)
    if ctx.obj['DEBUG']:
      raise e

@main.command()
@click.pass_context
@click.argument('token')
@click.option('--cluster-host', required=True, help="Hostname of the cluster to control")
@click.option('--cluster-ro', required=True, help="Cluster read-only service-account token")
@click.option('--cluster-rw', required=True, help="Cluster read-write service-account token")
@click.option('--vault', default='http://vault.local', help='Vault endpoint [http://vault.local]')
@click.option('--openshift', is_flag=True, default=False, help="Cluster is an Openshift distribution [False]")
@click.option('--init', is_flag=True, default=False, help="Initialize Vault [False]")
@click.option('--deploy', is_flag=True, default=False, help="Deploy agent and sentinel container automatically [False]")
@click.option('--vessel-api', default="http://cloud-api.oc.corp.sourcesense.com/rpc", help="Vessel API RPC endpoint [http://cloud-api.oc.corp.sourcesense.com/rpc]")
def register(ctx, token, cluster_host, cluster_ro, cluster_rw, vault, openshift, init, deploy, vessel_api):
  """
  Register workstaion to Vessel with the given TOKEN
  """
  payload = Payload(token)
  pipeline = Pipeline(start_fn=start, end_fn=end, prompt_fn=prompt)
  if init:
    pipeline.add(VaultInitStep(vault))
  pipeline.add(VaultSaveSecretsStep(vault, cluster_host, cluster_ro, cluster_rw, openshift))
  pipeline.add(GenerateKeysStep())
  pipeline.add(RegisterStep(vessel_api))
  pipeline.add(GenerateYamlStep())
  if deploy:
    pipeline.add(DeployAgentStep())
    pipeline.add(DeploySentinelStep())

  try:
    # Run pipeline
    payload = pipeline.run(payload)    
  except Exception as e:
    logger.error(e)
    if ctx.obj['DEBUG']:
      raise e
  

@main.command()
@click.pass_context
@click.argument('token')
@click.option('--dry', is_flag=True, default=False, help="Regenerates yaml files [False]")
def deploy(ctx, token, dry):
  """
  Deploy agent and sentinel for given TOKEN
  """
  click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))
  payload = Payload(token)
  pipeline = Pipeline(start_fn=start, end_fn=end, prompt_fn=prompt)
  pipeline.add(GenerateYamlStep())

  if not dry:
    pipeline.add(DeployAgentStep())
    pipeline.add(DeploySentinelStep())

  try:
    # Run pipeline
    payload = pipeline.run(payload)    
  except Exception as e:
    logger.error(e)
    if ctx.obj['DEBUG']:
      raise e

def patch_image(component, deployment, namespace, image, kube_apps):
  try:
      body = {
        "spec": {
          "template": {
            "spec": {
              "containers": [
                {
                  "name": deployment,
                  "image": image
                  }
              ]
            }
          }
        }
      }
      api_response = kube_apps.patch_namespaced_deployment(deployment, namespace, body)
  except ApiException as e:
      print("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)


@main.command()
@click.pass_context
@click.argument('token')
@click.option('--agent-tag', default=LATEST_AGENT, help="Set image tag for agent deployment")
@click.option('--sentinel-tag', default=LATEST_SENTINEL, help="Set image tag for sentinel deployment")
@click.option('--vault', default='http://vault.local', help='Vault endpoint [http://vault.local]')
def update(ctx, token, vault, sentinel_tag, agent_tag):
  """
  Updates agent and sentinel deployments
  """
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  payload = Payload(token)

  with open('/home/rke/.vessel/devops.json') as f:
    devops = json.load(f)

  with open(os.path.expanduser(f"~/.daas/{payload.token}/registration.json"), 'r') as f:
    registration = json.load(f)

  namespace = devops['vessel_namespace']
  img_base = devops['images_base_url']
  k8s_token = devops['devops_sa_token']
  cluster_name = sanitizeClusterName(registration['cluster']['result']['name'])
  
  # Init kube client
  click.echo('Creating kubernetes client configuration...')
  configuration = kubernetes.client.Configuration()
  configuration.host = devops['kubernetes_url']
  configuration.verify_ssl = False
  configuration.api_key = {"authorization": "Bearer " + k8s_token}
  api_client = kubernetes.client.ApiClient(configuration)
  apps = kubernetes.client.AppsV1Api(api_client)

  agent_deployment = cluster_name + '-agent'
  click.echo('Agent deployment name is %s' % agent_deployment)

  sentinel_deployment = cluster_name + '-sentinel'
  click.echo('Sentinel deployment name is %s' % sentinel_deployment)

  running_agent = apps.read_namespaced_deployment(agent_deployment, namespace).spec.template.spec.containers[0].image
  click.echo('At moment, you are running this tag image for Vessel Agent => ' + running_agent.split(":")[-1] )
  running_sentinel = apps.read_namespaced_deployment(sentinel_deployment, namespace).spec.template.spec.containers[0].image
  click.echo('At moment, you are running this tag image for Vessel Sentinel => ' + running_sentinel.split(":")[-1] )

  if running_agent.split(":")[-1] != agent_tag:
    click.echo('Updating Agent to tag ' + agent_tag)
    image = urljoin(img_base, 'workstation-agent') + ':' + agent_tag
    patch_image('Agent', agent_deployment, namespace, image, apps)
  else:
    click.echo('Agent is already updated')

  if running_sentinel.split(":")[-1] != sentinel_tag: 
    click.echo('Updating Sentinel to tag ' + sentinel_tag)
    image = urljoin(img_base, 'workstation-sentinel') + ':' + sentinel_tag
    patch_image('Sentinel', sentinel_deployment, namespace, image, apps)
  else:
    click.echo('Sentinel is already updated')
