import datetime

from termcolor import colored

from flag import Flag, await_
from handler import Handler
from cmd import Cmd


class CLI:
    def __init__(self) -> None:
        self.__msg_input: colored = colored('$', 'blue')
        self.__for_start_list: list = []
        self.__flag_list: list = []
        self.__cmd_list: list = []
        self.__last_cmd: str = ''
        self.__Handler = None
        self.Logger = None

        self.__copyright: bool = False
        self.turnOffCommand: list = []
        self.__full_log: bool = False
        self.__printlog: bool = False
        self.__debug: bool = False
        self.__time: bool = False
        self.copyright: str = ''

        self.__preCmd = None
        self.__postCmd = None
        self.__preRun = None

    def cmd(self, command: str, color: str = 'white', prefix: str = 'INFO', debug: bool = False):
        def wrapper(func):
            cmd = Cmd(func, command, color, prefix, debug)
            self.__for_start_list.append(cmd)
        return wrapper

    def run(self, full_log: bool = False, time: bool = False, printlog: bool = False, copyright: bool = False,
            debug: bool = False) -> None:

        self.__debug = debug
        self.__full_log = full_log
        self.__time = time
        self.__printlog = printlog
        self.__copyright = copyright

        self.Logger = Logger(self.__time)
        self.__Handler = Handler(self.__cmd_list, self.__flag_list, self.__full_log, self.__time, self.copyright, self.Logger)

        self.__for_start()
        self.__Handler.clear()
        self.__cmd_create()
        self.__flag_create()


        if self.__preRun:
            self.__preRun()

        if self.__copyright:
            print(self.copyright if self.copyright else 'Copyright is empty', end='\n\n')

        while True:
            command = input(self.__msg_input)

            if command:
                self.__Handler.handle(command, self.__preCmd, self.__postCmd)
                self.__last_cmd = command

    def __for_start(self):
        for cmd in self.__for_start_list:
            if cmd.mode and self.__debug:
                self.__cmd_list.append(cmd)
            elif not cmd.mode:
                self.__cmd_list.append(cmd)

    def __cmd_create(self) -> None:
        cmd_standart = {
            'help': {
                'func': self.__Handler.help,
                'command': 'help'},
            'exit': {
                'func': self.__Handler.exit,
                'command': 'exit'},
            'clear': {
                'func': self.__Handler.clear,
                'command': 'clear'},
            'quit': {
                'func': self.__Handler.quit,
                'command': 'quit'},
            'flags': {
                'func': self.__Handler.flags,
                'command': 'flags'},
            'colors': {
                'func': self.__Handler.color,
                'command': 'colors'},
            'copyright': {
                'func': self.__Handler.copyright,
                'command': 'copyright'},
            'version': {
                'func': self.__Handler.version,
                'command': 'version'},
            'case create': {
                'func': self.__Handler.case_create,
                'command': 'case create <name:str>'},
            'case run': {
                'func': self.__Handler.case_run,
                'command': 'case run <name:str>'},
            'case list': {
                'func': self.__Handler.case_list,
                'command': 'case list'}
                        }

        for cmd in cmd_standart:
            if cmd not in self.turnOffCommand:
                command = Cmd(cmd_standart[cmd]['func'], cmd_standart[cmd]['command'])
                self.__cmd_list.append(command)

    def __flag_create(self) -> None:
        flag_standart = {
            'await': {
                'func': await_,
                'command': '--await:<second:int>',
                'name': 'await'}
        }

        for flag in flag_standart:
            fl = Flag(flag_standart[flag]['name'], flag_standart[flag]['func'], flag_standart[flag]['command'])
            self.__flag_list.append(fl)

    def preCmd(self, func) -> None:
        self.__preCmd = func

    def postCmd(self, func) -> None:
        self.__postCmd = func

    def preRun(self, func) -> None:
        self.__preRun = func


class Logger:
    def __init__(self, time: bool) -> None:
        self.builtins = globals()["__builtins__"]
        self.builtin_print = self.builtins["print"]
        self.full_log_color: str = 'cyan'
        self.info_color: str = 'white'
        self.warning_color: str = 'yellow'
        self.error_color: str = 'red'
        self.time = time

    def info(self, msg: str, color: str = 'white', prefix: str = 'INFO') -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date = datetime.datetime.now()
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
            print(colored(msg, color))
        else:
            msg = colored(f'{prefix}: {msg}', color)
            print(msg)

    def warning(self, msg: str) -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date = datetime.datetime.now()
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] WARNING: {msg}'
            print(colored(msg, self.warning_color))
        else:
            msg = colored(f'WARNING: {msg}', self.warning_color)
            print(msg)

    def error(self, msg: str) -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date = datetime.datetime.now()
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] ERROR: {msg}'
            print(colored(msg, self.error_color))
        else:
            msg = colored(f'ERROR: {msg}', self.error_color)
            print(msg)


class ErrorMode(Exception):
    def __init__(self, text):
        self.text = text