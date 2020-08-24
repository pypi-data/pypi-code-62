import datetime
import re
import os

from termcolor import colored

from case import Case


class Handler:
    def __init__(self, cmd_list: list, flag_list: list, full_log: bool, time: bool, copyright: str, logger) -> None:
        self.colors: tuple = ('grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
        self.flag_list: list = flag_list
        self.copyright_: str = copyright
        self.full_log: bool = full_log
        self.cmd_list: list = cmd_list
        self.version_: str = '0.1.1'
        self.case_list_: list = []
        self.time: bool = time
        self.Logger = logger
        self.Type = Type(self.Logger)

    def handle(self, command: str, preCmd = None, postCmd = None) -> None:
        flag_list = []

        for flag in self.flag_list:
            fl = re.findall(flag.re, command)
            if len(fl) == 1:
                fl = fl[0]
                command = command.replace(f' {fl}', '').replace(f'{fl} ', '')
                arg = re.findall(':\\w+', fl)[0][1:]
                fl_arg = eval(f'{flag.args[0][1]}({arg})')
                flag_list.append((flag.func, {flag.args[0][0]: fl_arg, 'logger': self.Logger}))
            elif len(fl) > 1:
                msg = 'One flag can only be used once'
                self.Logger.warning(msg)

        res = self.found_cmd(command)
        if res:
            found_cmd, kwargs = res

            if flag_list:
                for flag in flag_list:
                    flag[0](**flag[1])

            if preCmd:
                preCmd()

            if found_cmd.cmd_args_inline:
                for arg in found_cmd.cmd_args_inline:
                    color = 'magenta'
                    if self.time:
                        date = datetime.datetime.now()
                        kwargs.update({arg[0]: self.Type.analis(input(colored(f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] INPUT: {arg[0]} - ', color)), arg[1])})
                    else:
                        kwargs.update({arg[0]: self.Type.analis(input(colored(f'INPUT: {arg[0]} - ', color)), arg[1])})

            found_cmd.run(**kwargs)

            if postCmd:
                postCmd()
        else:
            msg = f'Command \"{command}\" not found'
            self.Logger.warning(msg)

    def found_cmd(self, command) -> tuple:
        for cmd in self.cmd_list:
            res = re.findall(cmd.cmd_re, command)
            if res:
                res = res[0].split()
                kwargs = {}
                if cmd.cmd_args:
                    for index in range(len(cmd.cmd_args)):
                        kwargs.update({cmd.cmd_args[index][0]: self.Type.analis(res[cmd.cmd_args[index][2]],
                                                                                cmd.cmd_args[index][1])})

                return cmd, kwargs

    def help(self) -> None:
        """Help for commands"""

        prefix = 'HELP'
        color = 'green'
        tb = 111
        print()
        msg = f'"function name" {" "*6}|  "command"{tb*" "}  |  "documentation for the function"'
        self.Logger.info(msg, prefix=prefix, color=color)

        for cmd in self.cmd_list:
            tb_cmd = 120 - len(cmd.cmd_func)
            tb_name = 20 - len(cmd.func.__name__)
            msg = f'{cmd.func.__name__}{tb_name*" "}  |  {cmd.cmd_func}{tb_cmd*" "}  |  {cmd.func.__doc__}'
            self.Logger.info(msg, prefix=prefix, color=color)
        print()

    def flags(self) -> None:
        """Flags for commands"""

        prefix = 'FLAG'
        color = 'green'
        print()
        msg = f'"flag name" | "command" | "documentation for the function"'
        self.Logger.info(msg, prefix=prefix, color=color)

        for flag in self.flag_list:
            msg = f'"{flag.name}" | {flag.cmd} |' \
                  f' ({flag.args}) |' \
                  f' {flag.doc}'
            self.Logger.info(msg, prefix=prefix, color=color)
        print()

    def color(self) -> None:
        """A list of available colors for the output"""

        for color in self.colors:
            msg = f'name - {color}'
            prefix = 'COLOR'
            self.Logger.info(msg, prefix=prefix, color=color)

    def exit(self) -> None:
        """Exit"""

        color = 'cyan'
        if self.full_log:
            msg = f'Completion of work'
            self.Logger.info(msg, color=color)

        exit()

    def quit(self) -> None:
        """Quit"""

        color = 'cyan'
        if self.full_log:
            msg = f'Completion of work'
            self.Logger.info(msg, color=color)

        quit()

    def clear(self) -> None:
        """Clearing the terminal"""

        os.system('cls||clear')

    def copyright(self) -> None:
        """Output copyright"""

        if self.copyright_:
            print(self.copyright_, end='\n\n')
        else:
            msg = 'Copyright is empty'
            self.Logger.warning(msg)

    def version(self) -> None:
        """Displays the used version of the framework"""

        msg = f'py3_cli version {self.version_}'
        color = 'cyan'
        self.Logger.info(msg, color=color)

    def case_create(self, name: str) -> None:
        """Case create"""

        if name not in self.case_list_:
            case = []

            if self.full_log:
                prefix = 'CASE'
                color = 'cyan'
                msg = f'Case \"{name}\" created'
                if self.time:
                    date = datetime.datetime.now()
                    msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                    self.Logger.info(msg, prefix=prefix, color=color)
                else:
                    self.Logger.info(msg, prefix=prefix, color=color)

            while True:
                color = 'magenta'
                if self.time:
                    date = datetime.datetime.now()
                    command = input(colored(f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] INPUT: ', color))
                else:
                    command = input(colored(f'INPUT: ', color))

                if command == 'case end':
                    if case:
                        self.case_list_.append(Case(name, case))

                        if self.full_log:
                            prefix = 'CASE'
                            color = 'cyan'
                            msg = f'Case \"{name}\" closed'
                            if self.time:
                                date = datetime.datetime.now()
                                msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
                                self.Logger.info(msg, prefix=prefix, color=color)
                            else:
                                self.Logger.info(msg, prefix=prefix, color=color)
                        return
                else:
                    case.append(command)

        else:
            msg = 'A case with the same name already exists'
            self.Logger.warning(msg)

    def case_list(self) -> None:
        """List cases"""
        prefix = 'CASE'
        color = 'green'
        for case in self.case_list_:
            msg = f'{case.name} - {case.commands}'
            self.Logger.info(msg, prefix=prefix, color=color)

    def case_run(self, name) -> None:
        """Run case"""

        for case in self.case_list_:
            if case.name == name:
                for cmd in case.run():
                    self.handle(cmd)


class Type:
    def __init__(self, logger):
        self.Logger = logger

    def analis(self, arg, type_):
        if type_ == 'int':
            return self.int_(arg, type_)
        elif type_ == 'str':
            return arg
        elif type_ == 'bool':
            return self.bool_(arg, type_)
        elif type_ == 'bytes':
            return self.bytes_(arg, type_)
        else:
            msg = 'Invalid type'
            self.Logger.error(msg)
            exit()

    def int_(self, arg, type_):
        return eval(f'{type_}({arg})')

    def str_(self, arg, type_):
        return eval(f'{type_}({arg})')

    def bool_(self, arg, type_):
        return eval(f'{type_}({arg})')

    def bytes_(self, arg, type_):
        return eval(f'{type_}({arg})')