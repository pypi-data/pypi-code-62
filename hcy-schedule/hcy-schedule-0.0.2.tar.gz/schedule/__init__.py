import os
from time import time


class Schedule(object):

    def __init__(self, var, name='Process', width=''):

        if isinstance(var, int):
            self.__top = var
        elif isinstance(var, float):
            print(f'Warning: Total counter is not integer -> transform to integer by force')
            self.__top = int(var)
        elif isinstance(var, (list, dict, tuple, str, set)):
            self.__top = len(var)
        else:
            print(f'ERROR: Unrecognized type of variable to acquire total counter -> {type(var)}')
            exit(1)
        self.__start = time()
        self.__count = 0
        self.width = width

        if self.width != '':
            if self.width not in ['xs', 's', 'm', 'l', 'xl']:
                print(f'ERROR: Width can only be chosen from {["xs", "s", "m", "l", "xl"]}')
                exit(1)
            else:
                self.fix_width = True
                self.wmap = {
                    'xs': 50,
                    's': 70,
                    'm': 100,
                    'l': 130,
                    'xl': 150
                }
        else:
            self.fix_width = False
            try:
                self.__wchar = int(os.popen('stty size', 'r').read().split()[1]) - 1
            except Exception as e:
                print(f'Warning: Can not get width of terminal window, set to small default')
        self.__name = name

    def watch(self):
        if self.fix_width:
            self.__wchar = self.wmap[self.width]
        else:
            self.__wchar = int(os.popen('stty size', 'r').read().split()[1]) - 1
        self.__count += 1
        ratio = self.__count / float(self.__top)
        now_time = time()
        elapse = now_time - self.__start
        remain = elapse/ratio - elapse
        m, s = divmod(elapse, 60)
        h, m = divmod(m, 60)
        ET = 'ET='
        if h > 0:
            ET += f'{int(h)}:'
        if m > 0:
            ET += f'{int(m)}:'
        ET += f'{int(s)}s'
        m, s = divmod(remain, 60)
        h, m = divmod(m, 60)
        ETA = 'ETA<'
        if h > 0:
            ETA += f'{int(h)}:'
        if m > 0:
            ETA += f'{int(m)}:'
        ETA += f'{int(s)}s'
        head_bar = f'\r{self.__name}: {self.__count}/{self.__top} '
        tail_bar = f' {round(ratio * 100, 2)}% ' + ET + ' ' + ETA
        rest_char = self.__wchar - len(head_bar) - len(tail_bar) - 2
        pass_char = int(ratio * rest_char)
        process_bar = '[' + ('=' * (pass_char - 1)) + '>' + ('.' * (rest_char - pass_char)) + ']'
        watch_bar = head_bar + process_bar + tail_bar
        watch_bar += ' ' * (self.__wchar + 2 - len(watch_bar))
        if self.__count == self.__top:
            print(watch_bar)
        else:
            print(watch_bar, end='')

