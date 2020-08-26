# -*- coding: utf-8 -*-
import logging
import os
import sys
import click

from .config import DEFAULT_CONFIG, parse_config, load_config_file
from .router import StreamRouter
from .control.rcserver import RCServer

from odroute import __version__

logger = logging.getLogger(__name__)


@click.group()
@click.option('-v', '--verbose', default=False, is_flag=True)
def odr_cli(verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)

@odr_cli.command()
def version():
    click.echo(__version__)
    sys.exit()

@odr_cli.command()
@click.option('--config', '-c', 'config_file',
              # `type` is set to `str` and as we need to handle file reading manually (so not `click.File()`)
              type=str, required=False,
              help='Use the specified configuration file instead of CLI options'
              )
# sources (a.k.a. inputs) and outputs
@click.option('--source', '-s', 'source_ports',
              type=int, multiple=True, required=False,
              help='The source ports for incoming connections. Can (and likely will) be given multiple times'
              )
@click.option('--output', '-o', 'destinations',
              type=str, multiple=True, required=False,
              help='Destinations to route to, in the form of: tcp://<hostname>:<port>. Can be given multiple times'
              )
# no-audio and no-data failovers
@click.option('--delay', '-d', 'nodata_failover_delay',
              default=0.5,
              help='Delay for falling back to secondary streams in case of missing data'
              )
@click.option('--delay-recover', '-r', 'nodata_recover_delay',
              default=0.5,
              help='Delay for falling back to primary streams in case of recovery'
              )
@click.option('--audio-threshold', '-a', 'audio_threshold',
              default=-90,
              help='Minimum audio level (range [-90..0] dB) for input to be considered ok. Set to -90 to disable level detection'
              )
@click.option('--audio-delay', '-D', 'noaudio_failover_delay',
              default=10,
              help='Delay for falling back to secondary streams in case of audio level below threshold'
              )
@click.option('--audio-delay-recover', '-R', 'noaudio_recover_delay',
              default=10,
              help='Delay for falling back to primary streams in case of audio level recovery'
              )
# 'external' controls
@click.option('--telnet', '-t',
              required=False,
              help='Add telnet interface: <bind addr>:<port> or <port> (if only port is given interface will bind to 127.0.0.1)'
              )
@click.option('--socket', '-S',
              required=False,
              help='Add unix socket interface: </path/to/socket>'
              )
@click.option('--master', '-m',
              required=False,
              help='Connect odroute instance to master control-server: tcp://<hostnam>:<port>'
              )
def run(config_file, **config):

    #print(config)

    if config_file:
        config_file = os.path.abspath(config_file)
        click.echo('-' * 72)
        click.echo('Using config file - other CLI options will be ignored.\nConfig: {}'.format(config_file))
        click.echo('-' * 72)
        parsed_config = load_config_file(config_file)

    else:
        parsed_config = parse_config(config)


    # primitive logger configuration
    logging.basicConfig(
        format=parsed_config.get('log_format'),
        level=parsed_config.get('log_level'),
    )

    while True:
        r = StreamRouter(config=parsed_config)

        # adding remote-control interface
        telnet, socket = parsed_config.get('telnet', False), parsed_config.get('socket', False)
        if telnet or socket:
            rc_server = RCServer(router=r)

            if telnet:
                if telnet.isdigit():
                    _address, _port,  = '127.0.0.1', int(telnet)
                else:
                    _address, _port = telnet.split(':')

                logger.info('Binding telnet interface to {}:{}'.format(_address, _port))
                rc_server.bind(address=_address, port=int(_port))

            if socket:
                logger.info('Binding unix socket interface to {}'.format(socket))
                rc_server.add_unix_socket(socket)

            r.register_start_with_ioloop(rc_server)


        try:
            #r.connect()
            r.start()
        except KeyboardInterrupt:
            logger.info('Ctrl-c received. Stopping router.')
            r.stop()
            sys.exit()

