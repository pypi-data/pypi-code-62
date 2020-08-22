# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2020 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__all__ = ['Application', 'get_app']

import argparse
import sys
import traceback

from .baseobject import BaseObject, NonStdlibError
from .config import Config, ConfigError
from .log import configure as configurelog, getlog

#############################################################################


class ApplicationError (NonStdlibError):
    """Base exception for application errors"""
    pass


class OperationError (ApplicationError):
    """Raised when a runtime application operation fails"""
    pass


#############################################################################

_app_inst = None
_app_name = "UnamedApp"
_app_version = "0"


def get_app():
    global _app_inst
    return _app_inst


def _except_hook(exc_type, value, tb):
    global _app_name, _app_version

    try:
        log = getlog()
        log.critical('\n\nException: please include the following information '
                     'in any bug report:')
        log.critical('  %s version %s' % (_app_name, _app_version))
        log.critical('  Python version %s' % sys.version.split('\n', 1)[0])
        log.critical('')
        log.critical('Unhandled exception follows:')
        tblist = (traceback.format_tb(tb, None) +
                  traceback.format_exception_only(exc_type, value))
        if type(tblist) != list:
            tblist = [tblist, ]
        for lines in tblist:
            for line in lines.split('\n'):
                if not line:
                    continue
                log.critical('%s' % line.rstrip())
        log.critical('')
        log.critical('Please also include configuration information from '
                     'running %s' % _app_name)
        log.critical('with your normal options plus \'--dump\'')
    except: # noqa
        traceback.print_exception(exc_type, value, tb)


class Application (BaseObject):

    app_name = "UnnamedApp"
    app_version = "0"
    app_description = ""

    censored_config_params = None

    options = {'exception_hook': _except_hook,
               'argparse_kwargs': None,
               }

    def __init__(self, **kw):
        """constructor"""
        super(Application, self).__init__()
        self._parse_options(Application.options, kw)

        if hasattr(self, 'config_files'):
            self.app_config = self.config_files
        elif hasattr(self, 'config_file'):
            self.app_config = str(self.config_file)
        else:
            self.app_config = "%s.conf" % self.app_name

        global _app_inst, _app_name, _app_version
        _app_inst = self
        _app_name = self.app_name
        _app_version = self.app_version

        if self.exception_hook is not None:
            sys.excepthook = self.exception_hook

        self.cmdline_parser = self.build_cmdline_parser()
        self.additional_arguments = None

    def build_cmdline_parser(self):
        argparse_kwargs = self.argparse_kwargs or {}
        parser = argparse.ArgumentParser(description=self.app_description, **argparse_kwargs)
        parser.add_argument('--version',
                            action='version',
                            version='{0} {1}'.format(self.app_name, self.app_version))
        verbose_group = parser.add_mutually_exclusive_group()
        verbose_group.add_argument('-v', '--verbose',
                                   action='count',
                                   dest='verbose_level',
                                   default=1,
                                   help='Increase verbosity of output. Can be repeated.')
        verbose_group.add_argument('-q', '--quiet',
                                   action='store_const',
                                   dest='verbose_level',
                                   const=0,
                                   help='Supress output except warnings and errors.')
        parser.add_argument('--config',
                            action='store',
                            dest='app_config',
                            help='Specify an alternative config file to read.')
        parser.add_argument('--logfile',
                            action='store',
                            default=None,
                            help='Specify a file to log output. Disabled by default.')
        parser.add_argument('--debug',
                            default=False,
                            action='store_true',
                            help='Show tracebacks on errors.')
        parser.add_argument('--dump',
                            action='store_true',
                            help='Output configuration and other debugging information')
        return parser

    def start(self):
        try:
            self.cmdline_arguments, self.additional_arguments = self.cmdline_parser.parse_known_args(sys.argv[1:])
            if self.cmdline_arguments.app_config is not None:
                self.app_config = self.cmdline_arguments.app_config
            self.config = Config(self.app_config, censored_params=self.censored_config_params)
            if self.cmdline_arguments.dump:
                self.dump()

            configurelog(self.config, self.cmdline_arguments)

            self.setup(self.additional_arguments)
            self.run()
            self.cleanup()
            return 0

        except KeyboardInterrupt:
            self.abort('Aborted by user (keyboard interrupt)', errorcode=0)

        except ConfigError as o:
            self.abort('Configuration error: %s' % (o), errorcode=2)

        except OperationError as o:
            self.abort('Error: %s' % (o), errorcode=3)

        # otherwise, let the exception_hook handle the error (if defined)

    def setup(self, unknown_arguments):
        pass

    def cleanup(self):
        pass

    def run(self):
        raise NotImplementedError("Override this function to do something")

    def dump(self):
        sys.stdout.write('#########################################################\n')
        sys.stdout.write('# PACKMAKER DEBUG INFO DUMP:\n')
        sys.stdout.write('#    cmdline_arguments = {}\n'.format(self.cmdline_arguments))
        sys.stdout.write('#    additional_arguments = {}\n'.format(self.additional_arguments))
        sys.stdout.write('#    config filenames = {}\n'.format(self.config.filenames))
        sys.stdout.write('#    config contents:\n')
        self.config.dump_config(sys.stdout)
        sys.stdout.write('#########################################################\n')

    def abort(self, message, errorcode=1):
        sys.stderr.write('%s\n' % message)
        sys.stderr.flush()
        try:
            self.cleanup()
        except Exception as why:
            sys.stderr.write('UNEXPECTED ERROR during cleanup: %s\n' & str(why))
            sys.stderr.flush()
        sys.exit(errorcode)

#############################################################################
# THE END
