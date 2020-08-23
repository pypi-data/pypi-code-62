#!/usr/bin/env python

import sys
from . import __version__ as version


def print_version():
    print('WhatsAuto {}'.format(version))
    print('Python {}'.format(sys.version.replace('\n', ' ')))


def main():
    print_version()


if __name__ == "__main__":
    main()
