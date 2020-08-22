"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : filesniff.py
@Created : 2018-00-00
@Updated : 2020-08-21
@Version : 1.6.3
@Desc    : Get filepath in elegant way.
    Note: in this module getters' behaviors are somewhat different from
    `os.path` or `pathlib`, see below:
    1. `filesniff` uses '/' as path delimeter than '\\' in Windows.
    2. `filesniff` returns absolute path by default ways.
    3. `filesniff` promtes progressing speed at the expense of sacrificing path
       legality checking in some situations, it means `filesniff` would like to
       return a fake or a hypothetical path which doesn't really exist on
       system.
    4. `filesniff` assumes the callers would not pass any values what are beyond
       of expect, for example caller shouldn't pass '../!#$%?/./A.txt' as a path
       value (`filesniff` will not check path legality in some situations).
    5. Etc.
"""
import os
import sys

from typing import *


# ------------------------------------------------------------------------------
# Prettifiers

def prettify_dir(dirpath: str) -> str:
    return dirpath.replace('\\', '/').strip('/')


def prettify_file(filepath: str) -> str:
    return filepath.replace('\\', '/')


# ------------------------------------------------------------------------------
# Path Getters

def get_dirname(path: str) -> str:
    """ Input a dirpath or filepath, return the dirname.
    *We don't check the dirpath exists or not.*
    """
    if isdir(path):
        return path.rsplit('/', 1)[-1]
    else:
        if path.count('/') == 1:
            return path.split('/', 1)[0]
        else:
            return path.rsplit('/', 2)[-2]


def get_filename(filepath: str, suffix=True) -> str:
    """ Input a filepath, return the filename.
    The filepath can be absolute or relative, or just a filename.
    """
    if '/' in filepath:
        filepath = filepath.rsplit('/', 1)[-1]
    return filepath if suffix else filepath.rsplit('.', 1)[0]


def __get_launch_path() -> str:
    """ Get launcher's filepath.
    NOTE: this method only works in Pycharm.
    :return: e.g.
        sys.argv = ['D:\\myprj\\src\\main.py', ...] -> 'D:/myprj/src/main.py'
    """
    path = os.path.abspath(sys.argv[0])
    return prettify_file(path)


def __get_launch_dir() -> str:
    """ Get launcher's dirpath.
    NOTE: this method only works in Pycharm.
    :return: e.g. launcher = 'D:/myprj/src/main.py' -> 'D:/myprj/src'
    """
    dirpath = os.path.split(__get_launch_path())[0]
    return prettify_dir(dirpath)


def __get_prj_dir(working_dir=''):
    """ Get project dirpath.
    NOTE: This method only works in Pycharm.
    
    When script launched in Pycharm, the `sys.path[1]` is project's dirpath.
    If script launched in cmd or exe (pyinstaller), `_get_launch_dir()` is
    project's dirpath.
    """
    # prj dirpath
    if working_dir:
        dirpath = prettify_dir(os.path.abspath(working_dir))
    else:
        dirpath = prettify_dir(sys.path[1])
    # assert prj dirpath is launcher's parent path or launcher's itself.
    assert __get_launch_dir().startswith(dirpath), \
        'something wrong with `working_dir` (if you set it) or `sys.path[1]`'
    return dirpath


CURRDIR = __get_launch_dir()  # launcher's dirpath
PRJDIR = __get_prj_dir()  # project's dirpath


# usually PRJDIR == CURRDIR or CURRDIR.startswith(PRJDIR)


# ------------------------------------------------------------------------------
# Path Stitches

def stitch_path(*path_nodes, wrapper=None):
    """
    Use case:
        class FileReader:
            def __init__(self, path):
                self.holder = open(path, 'r')
                
        reader = stitch_path('D:', 'myprj', 'model', 'sample.txt', FileReader)
        # equals to: `reader = FileReader('D:/myprj/model/sample.txt')`
        
    :param path_nodes:
    :param wrapper:
    :return:
    """
    path = '/'.join(map(str, path_nodes))
    return path if wrapper is None else wrapper(path)


LKDB = prettify_dir(os.environ.get('LKDB', CURRDIR))  # dbpath


def lkdb(*subpath):
    """ Get path starswith os.environ['LKDB'].
    
    NOTE: you should preset Windows environment path:
        Key: LKDB
        Value (e.g.): D:\database
    Only works in Pycharm & Windows system.
    
    Tricks:
        # use '{PRJ}' as project name
        path = lkdb('{PRJ}', 'downloads')  # -> 'D:/database/myprj/downloads'
    """
    if subpath:
        return '{}/{}'.format(
            LKDB, '/'.join(map(str, subpath))
        ).replace(
            '{PRJ}', get_dirname(PRJDIR)
        )
    else:
        return LKDB


# ------------------------------------------------------------------------------
# Path Finders (File Finders)

def _find_paths(adir: str, path_type: str, fmt: str,
                suffix: Union[str, List, Tuple] = '', recursive=False,
                custom_filter=None):
    """ Base find method.
    
    :param adir: target path to find in.
    :param path_type: 'file'/'dir'.
    :param fmt: 'filepath'/'filename'/'zip'/'dict'/'dlist'.
        'filepath': return absolute filepaths.
            e.g. ['D:/A/B.txt', 'D:/A/C.txt', ...]
        'filename': return filenames only.
            e.g. ['B.txt', 'C.txt', ...]
        'zip': return zip(filenames, filepaths).
            e.g. zip(['B.txt', 'C.txt', ...], ['D:/A/B.txt', 'D:/A/C.txt', ...])
        'dict': return {filename: filepath}.
            e.g. {'B.txt': 'D:/A/B.txt', 'C.txt': 'D:/A/C.txt', ...}
        'dlist': return (filenames, filepaths).
            e.g. (['B.txt', 'C.txt', ...], ['D:/A/B.txt', 'D:/A/C.txt', ...])
    :param suffix: assign a filter to which file types we want to fetch.
        For example, we want only .txt files in target folder, then code like:
            _find_paths(target_folder, path_type='file', fmt='abspath',
                        suffix='.txt')
        Or we want .xlsx and .xlsm files:
            _find_paths(target_folder, path_type='file', fmt='abspath',
                        suffix=('.xlsx', '.xlsm'))
        NOTICE:
            1. Each suffix name must start with a dot ('.jpg', '.txt', etc.).
            2. The default schema of str-type is very casual! It means if we
               want .htm and .html files, just code:
                    _find_paths(target_folder, path_type='file', fmt='abspath',
                                suffix='.htm')
               It returns both .htm, .html and even anything matched `.htm*`!
               If it not as your expect, pls use list/tuple to constraint:
                    _find_paths(target_folder, path_type='file', fmt='abspath',
                                suffix=['.htm'])  # will only return .htm
            3. Not case sensitive.
        TLDR:
            - Use `suffix='.txt'` if you want to fetch .txt files by fuzzy
              match.
            - Use `suffix=['.txt', ...]` if you want to fetch multi-type files
              and by exact match.
    :param recursive: whether to find descendant folders.
        NOTICE: be careful if you set `fmt='dict'` & `recursive=True`, it is
        unsafe that some files with the same names will be overritten.
    :param custom_filter: if you want a more powerful filter than `suffix`
     param, set it here. The `custom_filter` works after `suffix` filter.
     Use case: see `find_subdirs()`, `findall_subdirs()`.
    :return:
    """
    adir = prettify_dir(adir)
    
    # recursive
    if recursive is False:
        names = os.listdir(adir)
        paths = (f'{adir}/{f}' for f in names)
        mix = zip(names, paths)
        if path_type == 'file':
            mix = filter(lambda x: os.path.isfile(x[1]), mix)
        else:
            mix = filter(lambda x: os.path.isdir(x[1]), mix)
    else:
        names = []
        paths = []
        for root, dirnames, filenames in os.walk(adir):
            root = prettify_dir(root)
            if path_type == 'file':
                names.extend(filenames)
                paths.extend((f'{root}/{f}' for f in filenames))
            else:
                names.extend(dirnames)
                paths.extend((f'{root}/{d}' for d in dirnames))
        mix = zip(names, paths)
    
    # suffix
    if suffix:
        if isinstance(suffix, str):
            mix = filter(lambda x: suffix in x[0], mix)  # fuzzy filter suffix
        elif isinstance(suffix, (tuple, list)):
            mix = filter(
                lambda x: '.' + x[0].rsplit('.', 1)[-1].lower() in suffix, mix
            )
        else:
            raise ValueError('Unknown suffix type', suffix, type(suffix))
    
    # custom_filter
    if custom_filter:
        mix = filter(custom_filter, mix)
    
    # fmt
    if fmt in ('filepath', 'dirpath', 'path'):
        return [y for x, y in mix]
    elif fmt in ('filename', 'dirname', 'name'):
        return [x for x, y in mix]
    elif fmt == 'zip':
        return mix
    elif fmt == 'dict':
        return dict(mix)
    elif fmt in ('dlist', 'list'):
        return zip(*mix)
    else:
        raise ValueError('Unknown fmt', fmt)


def find_files(adir, fmt='filepath', suffix=''):
    return _find_paths(adir, 'file', fmt, suffix, False)


def find_filenames(adir, suffix=''):
    return _find_paths(adir, 'file', 'filename', suffix, False)


def findall_files(adir, fmt='filepath', suffix=''):
    return _find_paths(adir, 'file', fmt, suffix, True)


def find_subdirs(adir, fmt='dirpath', suffix='',
                 exclude_protected_folder=True):
    """
    
    :param adir:
    :param fmt:
    :param suffix:
    :param exclude_protected_folder: exclude folders which startswith "." or
     "__" (e.g. ".git", ".idea", "__pycache__", etc.).
    :return:
    """
    
    def _filter(x):
        return not bool(x[0].startswith(('.', '__')))
    
    return _find_paths(
        adir, 'dir', fmt, suffix, False,
        _filter if exclude_protected_folder else None
    )


def findall_subdirs(adir, fmt='dirpath', suffix='',
                    exclude_protected_folder=True):
    """
    REF: https://www.cnblogs.com/bigtreei/p/9316369.html
    """
    
    def _filter(x):
        return not bool(x[0].startswith(('.', '__')))
    
    return _find_paths(
        adir, 'dir', fmt, suffix, True,
        _filter if exclude_protected_folder else None
    )


find_dirs = find_subdirs  # alias
findall_dirs = findall_subdirs  # alias


# ------------------------------------------------------------------------------
# Path Checks

def isfile(filepath: str) -> bool:
    """ Unsafe method judging path-like string.
    TLDR:
        If `filepath` looks like a filepath, will return True; otherwise return
         False.
    Judgement based:
        - Does it end with '/'? -> False
        - Does it really exist on system? -> True
        - Does it contain a dot ("xxx.xxx")? -> True
    Positive cases:
        print(isfile('D:/myprj/README.md'))  # -> True (no matter exists or not)
        print(isfile('D:/myprj/README'))  # -> True (if it really exists)
        print(isfile('D:/myprj/README'))  # -> False (if it really not exists)
    Negative cases: (the function judges seems not that good)
        print(isfile('D:/myprj/.idea'))  # -> True (it should be False)
        print(isfile('D:/!@#$%^&*/README.md'))  # -> True (it should be False)
    """
    if filepath == '':
        return False
    if filepath.endswith('/'):
        return False
    if os.path.isfile(filepath):
        return True
    if '.' in filepath.rsplit('/', 1)[-1]:
        return True
    else:
        return False


def isdir(dirpath: str) -> bool:
    """ Unsafe method judging dirpath-like string.
    TLDR:
        If `dirpath` looks like a dirpath, will return True; otherwise return
         False.
    Judgement based:
        - Is it a dot/dot-slash/slash? -> True
        - Does it really exist on system? -> True
        - Does it end with '/'? -> False
    """
    if dirpath == '':
        return False
    if dirpath in ('.', './', '/'):
        return True
    if os.path.isdir(dirpath):
        return True
    else:
        return False


# ------------------------------------------------------------------------------
# Path Getters 2

def _calc_path(base: str, offset: str):
    """ Calculate path by relative offset.
    The typical case is:
        base = 'D:/myprj', offset = 'model/sample.txt'
         -> return 'D:/myprj/model/sample.txt' (`return f'{base}/{offset}'`)
    :param base: absolute path
    :param offset: relative path (offset) to `base`
    :return:
    """
    if offset.startswith('./'):
        return f'{base}/{offset[2:]}'
    elif not offset.startswith('../'):
        return f'{base}/{offset}'
    else:
        segs1, segs2 = base.split('/'), offset.split('/')
        move_cnt = offset.count('..')
        return '/'.join(segs1[:-move_cnt] + segs2[move_cnt:])


def path_on_prj(offset: str):
    """ Calculate path based on PRJDIR as pivot.
    e.g. PRJDIR = 'D:/myprj', path = 'src/main.py' -> 'D:/myprj/src/main.py'
    """
    return _calc_path(PRJDIR, offset)


def path_on_self(offset: str, self: str = ''):
    """ Calculate path based on caller's `__file__` as pivot.
    
    :param offset:
    :param self: Recommended passing __file__ as value.
        E.g.
            # == D:/myprj/utils/abc.py ==
            from lk_utils import filesniff
            main_script = filesniff.path_on_self('../src/main.py', __file__)
            # -> main_script = 'D:/myprj/src/main.py'
        If `self` use default value (empty string), method will auto find out
        caller's path by analysing caller's Frame (this does the same result of
        `__file__` but consuming more time, so the default is not recommended.)
    :return:
    """
    if self == '':
        # noinspection PyProtectedMember,PyUnresolvedReferences
        frame = sys._getframe(1)
        self = frame.f_code.co_filename.replace('\\', '/')
    return _calc_path(prettify_dir(os.path.dirname(self)), offset)


getpath = get_path = path_on_prj  # alias
path_on_rel = path_on_self  # alias


# ------------------------------------------------------------------------------
# Other

def dialog(adir, suffix, prompt='请选择您所需文件的对应序号') -> str:
    """ File select dialog (Chinese). """
    print(f'当前目录为: {adir}')
    
    # fn: filenames, fp: filepaths
    fn, fp = find_files(adir, suffix, 'list')
    
    if not fn:
        raise FileNotFoundError(f'当前目录没有找到目标类型 ({suffix}) 的文件')
    
    elif len(fn) == 1:
        print(f'当前目录找到了一个目标类型的文件: {fn[0]}')
        return fp[0]
    
    else:
        x = ['{} | {}'.format(i, j) for i, j in enumerate(fn)]
        print('当前目录找到了多个目标类型的文件:'
              '\n\t{}'.format('\n\t'.join(x)))
        
        if not prompt.endswith(': '):
            prompt += ': '
        index = input(prompt)
        return fp[int(index)]


def create_dirpath(path: str):
    dirpath = (nodes := path.split('/'))[0]
    for node in nodes[1:]:
        dirpath += '/' + node
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
