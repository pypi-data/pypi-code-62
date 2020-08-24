import re


class Cmd:
    def __init__(self, func, cmd_func: str, color: str = 'white', prefix: str = 'INFO', mode: str = 'standart') -> None:
        self.cmd_func: str = cmd_func
        self.prefix: str = prefix
        self.color: str = color
        self.mode: str = mode
        self.func = func

        inline = get_args_inline(self.cmd_func)

        self.cmd_args_inline: list = inline[0]
        self.cmd_args: list = get_args(inline[1])
        self.cmd_re: str = get_regular(self.cmd_func)
        self.doc = func.__doc__

    def run(self, **kwargs) -> None:
        self.func(**kwargs)


def get_regular(cmd_func: str) -> str:
    found_args = re.findall('<\\w+:\\w+>', cmd_func)
    found_args_inline = re.findall('<\\w+:\\w+:\\w+>', cmd_func)

    for arg in found_args:
        cmd_func = cmd_func.replace(arg, '\\w+')

    for arg in found_args_inline:
        cmd_func = cmd_func.replace(' ' + arg, '')

    return cmd_func


def get_args(cmd_func: str) -> list:
    cmd = cmd_func.split()
    found_args = re.findall('<\\w+:\\w+>', cmd_func)
    args_list = [(re.findall('<\\w+:', arg)[0][1:-1],
                  re.findall(':\\w+>', arg)[0][1:-1],
                  cmd.index(arg)) for arg in found_args if found_args]

    return args_list


def get_args_inline(cmd_func: str) -> tuple:
    found_args = re.findall('<\\w+:\\w+:inline>', cmd_func)
    args_list = [(re.findall('<\\w+:', arg)[0][1:-1],
                  re.findall(':\\w+:', arg)[0][1:-1],
                  'inline') for arg in found_args if found_args]

    for arg in found_args:
        cmd_func = cmd_func.replace(f' {arg}', '')

    return args_list, cmd_func