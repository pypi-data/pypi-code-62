# -*- coding: utf-8 -*-
import logging
import re
import time

COMMANDS = [
    'help',
    'input.list',
    'input.list (?:[a-z]+)',
    'input.current',
    'input.force (?:[0-9]+|auto)',
    'input.add (?:[0-9]+)',
    'input.remove (?:[0-9]+)',
    'output.list',
    'output.list (?:[a-z]+)',
    'output.add (?:[a-z0-9\:\/]+)',
    'output.remove (?:[a-z0-9\:\/]+)',
    'reload',
]

# the quit command is implemented in rcserver.py
COMMANDS_HELP = '''
# odroute rc interface
  commands:
  quit:                        disconnect the RC control
  help:                        returns available list of commands
  input.list [detail]          returns router inputs [<port>]
  input.current                returns active input [<port>]
  input.force <port>|auto      force input on <port>; returns forced|auto input [<port>]
  input.add <port>             add input on port <port>
  input.remove <port>          removes input on port <port>
  output.list [detail]         returns router outputs [<tcp://host:port>]
  output.add <destination>     adds output to <tcp://host:port>
  output.remove <destination>  removes output <tcp://host:port>
  reload                       reloads configuration (only available if configured via file)
'''

logger = logging.getLogger(__name__)

class CommandExecutor(object):
    """
    implements a generic interface to send commands to the router instance.
    currently used by telnet and socket interface, partially implemented by
    `RoutingMinion`.
    implementation should use the `handle_command` method (see below) - however
    if you have reasons you can access the `router` directly at own risk.
    """

    router = None

    def __init__(self, router):
        self.router = router

    def handle_command(self, command):
        """
        handles incoming commands & calls respective methods
        input:
        `foo.bar abc xzz`
        is mapped to:
        `self.cmd_foo_bar(*['abc', 'xyz'])`
        """
        pattern = '(' + ')|('.join(COMMANDS) + ')'
        if not re.match(pattern, command):
            return 'invalid command. try "help"\n'

        _c = command.split(' ')
        _cmd, _args = _c[0].replace('.', '_'), _c[1:]

        try:
            return getattr(self, 'cmd_' + _cmd)(*_args)
        except (AttributeError) as e:
            logger.warning('error executing command {} - {}'.format(_cmd, e))
            return '{}'.format(e)

    ###################################################################
    # commands available through rc interface
    ###################################################################
    def cmd_help(self):
        """
        returns available list of commands
        """
        return COMMANDS_HELP

    def cmd_input_list(self, *args):
        """
        returns router inputs
        """
        result = ''

        if 'detail' in args:
            tmpl_h = "{port:7}{input:>6}{current:>8} {lastbeat:>10}{audio_left:>8}{audio_right:>8} {lastaudio:>10}\n"
            tmpl   = "{port:7}{input:>6}{current:>8} {lastbeat:10.2f}{audio_left:>8}{audio_right:>8} {lastaudio:>10.2f}\n"
            result += tmpl_h.format(
                    port="port",
                    input="input",
                    current="current",
                    lastbeat="last beat",
                    audio_left="audio l",
                    audio_right="audio r",
                    lastaudio="last audio")
            for input in self.router.get_inputs():
                audio_left, audio_right = input.frame_decoder.get_audio_levels()
                curr_in = self.router.get_current_input()
                result += tmpl.format(
                    port=input.port,
                    input='*' if input.is_available else '-',
                    current='*' if curr_in and curr_in.port == input.port else '-',
                    lastbeat=time.time() - input._last_beat,
                    audio_left=audio_left if audio_left is not None else "?",
                    audio_right=audio_right if audio_right is not None else "?",
                    lastaudio=time.time() - input._last_audio_ok
                )
        else:
            for input in self.router.get_inputs():
                result += '{}\n'.format(input.port)

        return result

    def cmd_output_list(self, *args):
        """
        returns router outputs
        """
        result = ''
        if 'detail' in args:
            for output in self.router.get_outputs():
                result += '{} {}\n'.format(output.output, output.is_connected())
        else:
            for output in self.router.get_outputs():
                result += '{}\n'.format(output.output)
        return result

    def cmd_output_add(self, *args):
        """
        Add input to router
        TODO: validate & handle exceptions
        """
        destination = args[0].strip()
        logger.debug('executor: output.add: {}'.format(destination))

        try:
            self.router.add_output(destination)
        except Exception as e:
            return "Could not add output: {}\n".format(e)
        return '{}\n'.format(destination)

    def cmd_output_remove(self, *args):
        """
        Add input to router
        TODO: validate & handle exceptions
        """
        destination = args[0].strip()
        logger.debug('executor: output.emove: {}'.format(destination))

        try:
            self.router.remove_output(destination)
        except Exception as e:
            return "Could not remove output: {}\n".format(e)
        return '{}\n'.format(destination)

    def cmd_input_current(self):
        """
        returns active router input
        """
        curr_in = self.router.get_current_input()
        if not curr_in:
            return 'none\n'
        return '{}\n'.format(curr_in.port)

    def cmd_input_force(self, *args):
        """
        Force input to given port, or switch back to "auto" mode
        """

        forced_port = args[0].strip()
        available_ports = [i.port for i in self.router.get_inputs()] + ['auto']

        if forced_port == 'auto':
            self.router.set_auto_switch()
            return 'auto\n'
        else:
            try:
                self.router.force_input(int(forced_port))
            except ValueError as e:
                return "Could not force port: {}\n".format(e)
            return '{}\n'.format(forced_port)

    def cmd_input_add(self, *args):
        """
        Add input to router
        TODO: validate & handle exceptions
        """
        port = int(args[0].strip())
        logger.debug('executor: input.add: {}'.format(port))

        try:
            self.router.add_input(port)
        except Exception as e:
            return "Could not add port: {}\n".format(e)
        return '{}\n'.format(port)

    def cmd_input_remove(self, *args):
        """
        Add input to router
        TODO: validate & handle exceptions
        """
        port = int(args[0].strip())
        logger.debug('executor: input.remove: {}'.format(port))
        self.router.remove_input(port)
        return '\n'


    def cmd_reload(self):
        """
        reload router configuration from config-file
        """
        logger.debug('executor: reload configuration')
        self.router.reload_configuration()
        return '\n'
