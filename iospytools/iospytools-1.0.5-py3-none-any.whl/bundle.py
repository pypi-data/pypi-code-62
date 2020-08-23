import os
import plistlib

try:
    import bsdiff4
except ImportError:
    raise


class Bundle:
    def __init__(self, bundle: str):
        super().__init__()

        try:
            with open('{}/Info.plist'.format(bundle), 'rb') as f:
                self.plist = plistlib.load(f)
        except FileNotFoundError:
            print('Info.plist does not exist!')
            raise

    def parsePlist(self):
        return self.plist
