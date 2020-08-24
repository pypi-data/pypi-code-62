import os
import pathlib


class AutoRemovablePath(pathlib.Path):
    """
    This class overrides context manager behavior of the original pathlib.Path class.
    If a dir or a file is open using the 'with' statement
    it will be automatically removed after leaving a corresponding context manager.
    Everything else works exactly like in  the original pathlib.Path class.

    Compatibility note: this has been developed & tested under Python 3.7.2 on Win 10 and Ubuntu 20.04
    so it will be working fine with any Python 3.7 & older.
    I also assume that it will be working fine with any Python3.* .
    """

    # All credits for this solution with _flavour go to https://stackoverflow.com/a/53231179/12444061

    # PyCharm marks this _flavour statement as containing unresolved references
    # noinspection PyUnresolvedReferences
    _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

    def remove_dir_recursively(self) -> None:
        """
        Removes dir recursively exactly like 'rm -r' from Bash.


        :return: None

        :rtype: None

        :raises: Will raise a TypeError if self is not a dir.
        """
        # Modified solution from https://stackoverflow.com/a/57892171/12444061
        if self.is_dir():

            for child in self.glob('*'):  # Iterating over each sub-file or sub-dir
                child.unlink() if child.is_file() else AutoRemovablePath(child).remove_dir_recursively()  # Removes a
                # file if a child is a file, else recursively removes sub-dir

            self.rmdir()  # Removing this dir. It will be empty by the time

        else:
            raise TypeError(f'Not a dir')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_dir_recursively() if self.is_dir() else self.unlink()
