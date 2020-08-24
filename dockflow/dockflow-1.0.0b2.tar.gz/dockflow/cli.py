import click
import os
import logging
import docker

docker_client = docker.from_env()
cwd = os.getcwd()
airflow_home = "/usr/local/airflow"


def check_config(config_file):
    filename = os.path.expanduser(config_file)
    if os.path.exists(filename):
        with open(filename) as cfg:
            image_repo = cfg.read().strip('\n')
        return image_repo
    else:
        click.secho("Use `dockflow config` to set container repo", fg='red')


def copy_to_docker(name):
    os.system("docker cp " + cwd + "/" + name + " " + prefix(cwd) + "-airflow:" + airflow_home + "/" + name)


def dir_exist(directory):
    return os.path.exists(directory)


def prefix(directory):
    last_path = os.path.split(directory)
    container_prefix = last_path[1]
    return container_prefix


def ask_user(question):
    check = str(input(question + "(Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user(question)
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user(question)


@click.group()
def main():
    """
        Spatialedge Airflow Development CLI \n
        Version: 1.0.0beta2
    """
    pass


@main.command()
@click.option(
    '-iv',
    '--image-version',
    help='Specify Cloud Composer Airflow version',
    type=str,
    default="composer-1.10.6-airflow-1.10.6",
)
@click.option(
    '--config-file',
    '-c',
    type=click.Path(),
    default='~/.dockflow/dockflow.cfg',
)
@click.option(
    '--gcp-creds',
    '-creds',
    type=click.Path(),
    default='~/.dockflow/gcp_credentials.json'
)
def start(image_version, config_file, gcp_creds):
    """
        Start Airflow instance
    """
    volumes = {}
    click.secho('Checking if container {}-airflow is already running'.format(prefix(cwd)), fg='green')
    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'running'}):
        click.secho("Container {}-airflow already running".format(prefix(cwd)), fg='green')
    elif docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow"), 'status': 'exited'}):
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        container.start()
        if dir_exist(cwd + "/airflow.db"):
            copy_to_docker("airflow.db")
            container.exec_run("chown airflow " + airflow_home + "/airflow.db", user='root')
        click.secho("Container {}-airflow started".format(prefix(cwd)), fg='green')

    else:
        click.secho('Starting container {}-airflow:{} creation'.format(prefix(cwd), image_version.strip('=')), fg='green')

        version = image_version.strip('=')
        image_repo = check_config(config_file)
        click.secho("Checking if image is up-to-date...", fg='green')
        os.system("docker pull " + image_repo + ":" + version)
        click.secho('Checking if "dags" folder exists', fg='green')
        if dir_exist(cwd + "/dags/"):
            volumes[cwd + '/dags/'] = {'bind': airflow_home + '/dags/', 'mode': 'rw'}
            click.secho('"dags" folder found', fg='green')

            click.secho('Checking if "scripts" directory exists and mount if exist', fg='green')
            if dir_exist(cwd + "/scripts/"):
                volumes[cwd + '/scripts/'] = {'bind': airflow_home + '/scripts/', 'mode': 'rw'}
                click.secho('"scripts" directory mounted', fg='cyan')
            click.secho('Checking if "tests" directory exists and mount if exist', fg='green')
            if dir_exist(cwd + "/tests/"):
                volumes[cwd + '/tests/'] = {'bind': airflow_home + '/tests/', 'mode': 'rw'}
                click.secho('"tests" directory mounted', fg='cyan')
            container = docker_client.containers.create(
                image_repo + ":" + version,
                ports={'8080/tcp': 8080,
                       '5432/tcp': 5432,
                       },
                volumes=volumes,
                name=prefix(cwd) + '-airflow',
            )
            click.secho('Container {}-airflow:{} created'.format(prefix(cwd), version), fg='green')

            click.secho('Check if GCP credentials exist and mount if exists', fg='green')
            creds = os.path.expanduser(gcp_creds)
            if dir_exist(creds):
                click.secho('Mounting GCP credentials: {}'.format(creds), fg='cyan')
                os.system(
                    "docker cp " + creds + " " + prefix(cwd) + "-airflow:" + airflow_home + "/gcp_credentials.json")
            else:
                click.secho('GCP Credential file {} not found, will not mount to container'.format(creds), fg='red')

            container.start()

            click.secho('Check if local airflow.db exist and copy if exist', fg='green')
            if dir_exist(cwd + "/airflow.db"):
                copy_to_docker("airflow.db")
                container.exec_run("chown airflow " + airflow_home + "/airflow.db", user='root')
                click.secho('Local airflow.db mounted to container', fg='cyan')

            click.secho("Container {}-airflow:{} started".format(prefix(cwd), version), fg='green')
        else:
            click.secho("DAGs directory not found! \nAre you in the root directory of your project?", fg='red',
                        bold=True)


@main.command()
@click.option(
    '--rm',
    is_flag=True
)
def stop(rm):
    """
        Stop Airflow instance
    """
    click.secho('Persisting Airflow db', fg='green')
    os.system("docker cp " + prefix(cwd) + "-airflow:" + airflow_home + "/airflow.db " + cwd + "/airflow.db")
    logging.info("Stopping Airflow instance mounted to current directory")
    if docker_client.containers.list(filters={'name': (prefix(cwd) + "-airflow")}):
        container = docker_client.containers.get(prefix(cwd) + "-airflow")
        click.secho("Stopping container...", fg='red')
        container.stop()
        if rm:
            container.remove()
            click.secho("Container " + prefix(cwd) + "-airflow stopped and removed", fg='red')
        else:
            click.secho("Container " + prefix(cwd) + "-airflow stopped", fg='red')
    else:
        click.secho("Nothing to stop.", fg='red')


@main.command()
def refresh():
    """
        Run refresh/bundling scripts
    """
    container = docker_client.containers.get(prefix(cwd) + "-airflow")
    if dir_exist(cwd + "/scripts/"):
        click.secho("Refreshing dags...", fg='green')
        for f in os.listdir(cwd + "/scripts/"):
            CONTAINER_PATH = airflow_home + "/scripts/" + f
            container.exec_run("python " + CONTAINER_PATH, user="airflow")
        click.secho("All DAGs refreshed", fg='green')
    else:
        click.secho("Either not project root directory or no 'scripts' folder present", fg='red')


@main.command()
def config():
    """
        Store container repo URL
    """
    # Check whether config dir exists
    config_dir = os.path.expanduser('~/.dockflow')
    if dir_exist(config_dir) is False:
        os.mkdir(config_dir)
    # Prompt user for input
    image_repo = click.prompt(
        "Please enter your container repo URL",
    )
    # Write to config file
    config_file = os.path.expanduser('~/.dockflow/dockflow.cfg')
    with open(config_file, 'w') as cfg:
        cfg.write(image_repo)


@main.command()
def reset():
    """
        Reset Airflow db
    """
    container = docker_client.containers.get(prefix(cwd) + "-airflow")
    if ask_user("Are you sure?"):
        click.secho("Resetting Airflow database...", fg='green')
        container.exec_run("airflow resetdb -y")
        click.secho("Restarting container...", fg='green')
        container.stop()
        container.start()
        click.secho("Airflow db reset completed", fg='green')


@main.command()
def dashboard():
    """
        Open Airflow in default browser
    """
    click.launch('http://localhost:8080')


@main.command()
def test():
    """
        Run tests located in tests dir if test.sh exists
    """
    container = docker_client.containers.get(prefix(cwd) + "-airflow")
    if dir_exist(cwd + "/test.sh"):
        copy_to_docker("test.sh")
        container.exec_run("chown airflow " + airflow_home + "/test.sh", user='root')
        container.exec_run("chmod +x " + airflow_home + "/test.sh", user='root')
        click.secho("Executing test.sh", fg='green')
        os.system("docker exec " + prefix(cwd) + "-airflow ./test.sh")
    else:
        click.secho("No test script found...", fg='red')
        click.secho("Ensure you are in the project root directory and `test.sh` exists", fg='red')
