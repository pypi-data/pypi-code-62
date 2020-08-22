import importlib
import os
import subprocess
from configparser import ConfigParser
from datetime import datetime

from oort.shared.config import (
    get_config_socket_file_path,
    get_logger,
    get_oort_config_file_path, get_supervisor_conf_file_path,
    get_supervisord_log_file_path
)
from oort.shared.utils import get_username

SERVER_PROCESS = 'oort-server'
UPLOADER_PROCESS = 'oort-uploader'
DEFAULT_PROCESSES = [SERVER_PROCESS, UPLOADER_PROCESS]


# noinspection OsChmod
def configure_supervisor(debug=False):
    logger = get_logger(debug=debug)
    logger.debug(f'Configuring supervisord debug={debug}...')

    conf_file_path = get_supervisor_conf_file_path()
    if not os.path.exists(conf_file_path):
        output = subprocess.run(["echo_supervisord_conf"], capture_output=True, text=True)
        with open(conf_file_path, "w") as f:
            f.write(output.stdout)

    conf = ConfigParser()
    conf.read(conf_file_path)

    # section: unix_http_server
    conf.set('unix_http_server', 'file', get_config_socket_file_path())
    conf.set('unix_http_server', 'chmod', '0760')
    conf.set('unix_http_server', 'user', get_username())

    # section: supervisord:
    conf.set('supervisord', 'logfile', get_supervisord_log_file_path())
    conf.set('supervisord', 'user', get_username())

    # section: supervisorctl
    conf.set('supervisorctl', 'serverurl', 'unix://' + get_config_socket_file_path())
    conf.set('supervisorctl', 'user', get_username())

    # section: inet_http_server
    if 'inet_http_server' not in conf.sections():
        conf.add_section('inet_http_server')
    conf.set('inet_http_server', 'port', '127.0.0.1:9001')

    spec = importlib.util.find_spec('oort')
    for command in ['server', 'uploader']:
        command_path = os.path.join(os.path.dirname(spec.origin), command, 'main.py')
        # Making sure they are executable
        os.chmod(command_path, 0o744)

        section_name = f'program:oort-{command}'
        if section_name not in conf.sections():
            conf.add_section(section_name)

        if debug is True:
            command_path += ' --debug'

        conf.set(section_name, 'command', 'python3 ' + command_path)
        conf.set(section_name, 'user', get_username())
        conf.set(section_name, 'autostart', 'true')
        conf.set(section_name, 'autorestart', 'true')

    with open(conf_file_path, 'w') as f:
        conf.write(f)

    # Save details about config

    conf = ConfigParser()
    conf.read(get_oort_config_file_path())
    if 'supervisor' not in conf.sections():
        conf.add_section('supervisor')
    version = subprocess.check_output(["oort", "--version"]) or ''
    conf.set('supervisor', 'config', version.decode('utf8').strip())
    conf.set('supervisor', 'date', datetime.now().isoformat())
    with open(get_oort_config_file_path(), 'w') as f:
        conf.write(f)

    logger.debug('Configuration done.')


def check_config_version(debug=False):
    raw_current_version = subprocess.check_output(["oort", "--version"]) or ''
    current_version = raw_current_version.decode('utf8').strip()
    conf = ConfigParser()
    conf.read(get_oort_config_file_path())
    config_version = conf.get('supervisor', 'version')
    if config_version != current_version:
        logger = get_logger(debug=debug)
        logger.warn(f'Config version {config_version} is obsolete (new: {current_version}). Run `oort reload`.')


def start_supervisor_daemon(debug=False):
    logger = get_logger(debug=debug)
    logger.debug('Starting supervisord...')

    conf_file_path = get_supervisor_conf_file_path()
    output = subprocess.run(["supervisord", "-c", conf_file_path], capture_output=True, text=True)

    if "Error: Another program is already listening" in output.stderr:
        p1 = subprocess.Popen(['lsof', '-i', ':9001'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "LISTEN"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["awk", "{print $2}"], stdin=p2.stdout, stdout=subprocess.PIPE, text=True)
        output = p3.communicate()
        port_9001_process_pid = output[0].strip()

        p1 = subprocess.Popen(['lsof', '-a', f'-p{port_9001_process_pid}'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "supervisor.sock"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
        port_9001_processes = p2.communicate()

        if len(port_9001_processes[0]) > 0:
            print('Supervisor is already running. Fine.')
        else:
            print('Supervisor usual port (9001) is already taken by another process.')

    elif len(output.stderr) > 0:
        print(output.stderr)

    elif len(output.stdout) > 0:
        logger.debug(output.stdout)

    subprocess.run(["supervisorctl", "reload"])
    logger.debug('Daemon start done.')


def start_supervisor_processes(*args, debug=True):
    logger = get_logger(debug=debug)
    logger.debug('Starting Oort processes...')
    if len(args) == 0:
        args = DEFAULT_PROCESSES
    subprocess.run(["supervisorctl", "start"] + list(args))
    logger.debug('Start done.')


def stop_supervisor_processes(*args, debug=True):
    logger = get_logger(debug=debug)
    if len(args) == 0:
        args = DEFAULT_PROCESSES
    logger.debug('Getting status of Oort processes...')
    subprocess.run(["supervisorctl", "stop"] + list(args))
    logger.debug('Stop done.')


def restart_supervisor_processes(*args, debug=True):
    logger = get_logger(debug=debug)
    if len(args) == 0:
        args = DEFAULT_PROCESSES
    logger.debug('Restarting Oort processes...')
    subprocess.run(["supervisorctl", "restart"] + list(args))
    logger.debug('Restart done.')


def get_supervisor_processes_status(*args, debug=True):
    logger = get_logger(debug=debug)
    logger.debug('Getting status of Oort processes...')
    subprocess.run(["supervisorctl", "status"] + list(args))
    logger.debug('Getting status done.')
