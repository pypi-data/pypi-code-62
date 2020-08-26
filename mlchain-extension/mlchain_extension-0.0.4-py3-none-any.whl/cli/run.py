import click
import os
import signal
from mlchain import logger
import GPUtil
from mlchain.cli.run import get_model
from mlchain_extension.queue.redis.server import RedisQueue


def select_gpu():
    try:
        gpus = GPUtil.getFirstAvailable()
    except:
        gpus = []
    if len(gpus) == 0:
        gpus = [0]
    while True:
        for gpu in gpus:
            yield str(gpu)


op_config = click.option("--config", "-c", default=None, help="file json or yaml")
op_name = click.option("--name", "-n", default=None, help="name service")
op_redis = click.option('--redis', 'queue', flag_value='redis')
op_worker = click.option('--workers', '-w', 'workers', default=1, type=int)
op_mode = click.option('--mode', '-m', 'mode', default=None, type=str)


@click.command("run", short_help="Run a development server.")
@click.argument('entry_file', nargs=1, required=False, default=None)
@op_redis
@op_worker
@op_config
@op_name
@op_mode
@click.option('--function_name','-f',multiple=True)
def run_command(entry_file, name, queue, workers, mode, config, function_name):
    from mlchain import config as mlconfig
    default_config = False
    if config is None:
        default_config = True
        config = 'mlconfig.yaml'
    if os.path.isfile(config):
        if config.endswith('.json'):
            config = mlconfig.load_json(config)
        elif config.endswith('.yaml') or config.endswith('.yml'):
            config = mlconfig.load_yaml(config)
        else:
            raise AssertionError("Not support file config {0}".format(config))
    else:
        if not default_config:
            raise FileNotFoundError("Not found file {0}".format(config))
        config = {}
    if 'mode' in config and 'env' in config['mode']:
        if mode in config['mode']['env']:
            config['mode']['default'] = mode
    mlconfig.load_config(config)
    entry_file = mlconfig.get_value(entry_file, config, 'entry_file', 'server.py')
    queue = mlconfig.get_value(queue, config, 'queue', None)
    workers = mlconfig.get_value(workers, config, 'workers', None)
    name = mlconfig.get_value(name, config, 'name', None)
    version = mlconfig.get_value(None, config, 'version', '0.0')
    version = str(version)
    if len(function_name) == 0:
        function_name = None
    function_name = mlconfig.get_value(function_name, config, 'function_name', None)
    import logging
    logging.root = logging.getLogger(name)
    logger.debug(dict(
        entry_file=entry_file,
        queue=queue,
        workers=workers,
        name=name,
        mode=mode,
        function_name=function_name
    ))
    serve_model = get_model(entry_file, serve_model=True)
    RedisQueue(serve_model, name=name, version=version, config=function_name).run()
