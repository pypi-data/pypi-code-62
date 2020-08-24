"""tools for indirect run control of ChemStation"""
import re
import time
import pathlib
import logging
import threading
import warnings

from typing import Union, Tuple, List
from .config import CHEMSTATION_DATA_PATHS


logger = logging.getLogger(__name__)

# acquiring parser
_acq_re = re.compile(
    'CURRDATAFILE:(?P<file_number>\d+)\|(?P<file_name>[^\n]+)'
)


class AGDataPath:
    # list of AGDataPaths
    _paths: List['AGDataPath'] = []

    def __init__(self,
                 data_path: Union[str, pathlib.Path],
                 cycle_time: float = 1.
                 ):
        """
        An Agilent ChemStation data path monitoring class. This class will monitor for sequence flags and will live-update
        acquiring status, the current data file, and the current sample number.

        :param data_path: file path to the data directory
        :param cycle_time: cycle time to check for updates to the file
        """
        if isinstance(data_path, pathlib.Path) is False:
            data_path = pathlib.Path(data_path)
        self.data_parent = data_path
        self._acquiring_path: pathlib.Path = None
        self._current_number: int = None
        self._current_file: str = None
        self.cycle_time = cycle_time
        self._monitor_thread = threading.Thread(
            target=self.acquiring_monitor,
            daemon=True,
        )
        self._killswitch = threading.Event()
        if self not in self._paths:
            self._paths.append(self)

    def __eq__(self, other: Union[str, 'AGDataPath']):
        if isinstance(other, AGDataPath):
            return self.data_parent == other.data_parent
        elif type(other) is str:
            return str(self.data_parent) == other
        else:
            return False

    def __str__(self):
        out = f'{self.data_parent}'
        if self.acquiring is True:
            out += ' ACQUIRING'
        return out

    def __repr__(self):
        return f'{self.__class__.__name__} {self.data_parent} {"ACQUIRING" if self.acquiring else ""}'

    @property
    def acquiring_path(self) -> pathlib.Path:
        """path to the acquiring file"""
        return self._acquiring_path

    @property
    def current_number(self) -> int:
        """current acquiring number indicated in acquiring file"""
        return self._current_number

    @property
    def current_file(self) -> pathlib.Path:
        """currently acquiring file indicated in acquiring file"""
        if self._current_file is not None:
            return self._acquiring_path.parent / self._current_file

    @property
    def acquiring(self) -> bool:
        """whether acquiring is indicated in the target directory"""
        return self.acquiring_path is not None

    @property
    def subdirectories(self) -> List[pathlib.Path]:
        """subdirectories of the root folder"""
        return [
            directory
            for directory in self.data_parent.iterdir()
            if directory.is_dir()
        ]

    @property
    def newsorted_subdirectories(self) -> List[pathlib.Path]:
        """subdirectories of the root path sorted by date modified in newest to oldest order"""
        return sorted(
            self.subdirectories,
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

    def locate_acquiring(self):
        """
        Locates ACQUIRING.TXT files in the directory. This file appears when ChemStation is acquiring
        a sequence.

        :return:
        """
        out = []
        for subdir in self.newsorted_subdirectories:
            for file in subdir.glob('**/ACQUIRING.TXT'):
                out.append(file)
        return out

    @staticmethod
    def current_num_and_file(path: Union[str, pathlib.Path]) -> Tuple[int, str]:
        """
        Returns the current number in the sequence and the name of the data file being acquired.

        :param path: path to parse
        :return: current file number, current file name
        """
        with open(path, 'rt', encoding='utf16') as f:
            contents = f.read()
        match = _acq_re.search(contents)
        if match is None:
            raise ValueError('The contents of ACQUIRING.TXT could not be parsed.')
        return (
            int(match.group('file_number')),
            match.group('file_name')
        )

    def acquiring_monitor(self):
        """
        Searches for and monitors acquiring files in the target directory.
        """
        while True:
            if self._killswitch.isSet():
                break

            # if the acquiring path is None
            if self._acquiring_path is None:
                # logger.debug('attempting to locate acquiring file')
                acquiring_paths = self.locate_acquiring()
                # if there is more than one file, something is wrong
                if len(acquiring_paths) > 1:
                    logger.error('multiple matches found')
                    raise ValueError(
                        f'{len(acquiring_paths)} matches for ACQUIRING.TXT were found in the directory '
                        f'{self.data_parent}. This usually results when ChemStation did not exit cleanly. Please locate and '
                        f'remove the old acquiring file. '
                    )
                # if there is one file, update
                elif len(acquiring_paths) == 1:
                    logger.info('ACQUIRING.TXT located')
                    self._acquiring_path = acquiring_paths[0]
                    continue

                # if no files
                else:
                    # logger.debug('no acquiring file located')
                    continue

            # if the file has disappeared, set to None
            if self._acquiring_path.is_file() is False:
                logger.info('ACQUIRING.TXT disappeared')
                self._acquiring_path = None
                continue

            # todo verify that this always works
            # parse and retrieve current number and file
            try:
                self._current_number, self._current_file = self.current_num_and_file(self._acquiring_path)
            except (ValueError, PermissionError) as e:
                logger.debug(e)
                self._current_number = None
                self._current_file = None

            # wait cycle time
            time.sleep(self.cycle_time)

    def start_monitor(self):
        """starts the acquiring monitor thread"""
        logger.info('starting acquiring monitor')
        self._monitor_thread.start()

    def kill_monitor(self):
        """cleanly terminates the monitor thread"""
        self._killswitch.set()

    @classmethod
    def currently_acquiring_paths(cls) -> List['AGDataPath']:
        """Retrieves a list of currently acquiring data paths"""
        return [
            data_path
            for data_path in cls._paths
            if data_path.acquiring is True
        ]

    @classmethod
    def start_monitoring_all_paths(cls):
        """starts the monitor thread on all data paths"""
        logger.debug('starting all monitor threads')
        for data_path in cls._paths:
            data_path.start_monitor()

    @classmethod
    def kill_all_monitors(cls):
        """terminates all monitor threads"""
        logger.debug('terminating all monitor threads')
        for data_path in cls._paths:
            data_path.kill_monitor()


def sequence_is_running() -> bool:
    """returns whether a sequence is running"""
    warnings.warn(  # v4.4.0
        'sequence_is_running will be deprecated, access AGDataPath properties instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return len(AGDataPath.currently_acquiring_paths()) > 0


def current_num_and_file() -> Tuple[int, str]:
    """
    Returns the current number in the sequence and the name of the data file being acquired.

    :return: current file number, current file name
    """
    warnings.warn(  # v4.4.0
        'current_num_and_file will be deprecated, access AGDataPath properties instead',
        DeprecationWarning,
        stacklevel=2,
    )
    currently_acquiring = AGDataPath.currently_acquiring_paths()
    if len(currently_acquiring) > 1:
        raise ValueError('more than one sequence is currently acquiring')
    return (
        currently_acquiring[0].current_number,
        str(currently_acquiring[0].current_file),
    )


def current_file() -> str:
    """
    Returns the current data file name being acquired (next up in the sequence)

    :return: data file name
    """
    warnings.warn(  # v4.4.0
        'current_file will be deprecated, access AGDataPath properties instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return current_num_and_file()[1]


def current_file_path() -> pathlib.Path:
    """
    Returns the full path for the file name being acquired (next up in the sequence)

    :return: full path to the data file
    """
    warnings.warn(  # v4.4.0
        'current_file_path will be deprecated, access AGDataPath properties instead',
        DeprecationWarning,
        stacklevel=2,
    )
    currently_acquiring = AGDataPath.currently_acquiring_paths()
    if len(currently_acquiring) > 1:
        raise ValueError('more than one sequence is currently acquiring')
    current_path = currently_acquiring[0]
    return current_path.current_file


# automatically instantiate defined data paths
acquiring_monitors: List[AGDataPath] = [
    AGDataPath(path)
    for path in CHEMSTATION_DATA_PATHS
]
