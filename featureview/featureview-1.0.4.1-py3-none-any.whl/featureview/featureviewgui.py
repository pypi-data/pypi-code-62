# -*- coding:utf-8 -*-
"""
mes err refer to
https://stackoverflow.com/questions/32966226/how-solve-qt-untested-windows-version-10-0-detected
"""
import argparse
import sys
from PyQt5 import QtWidgets

from featureview.widget.login import Window


def _cmd_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--measurements',
        nargs='*',
        help='list of measurement files',
    )
    return parser


def main(measurements=None):
    parser = _cmd_line_parser()
    args = parser.parse_args(sys.argv[1:])
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
