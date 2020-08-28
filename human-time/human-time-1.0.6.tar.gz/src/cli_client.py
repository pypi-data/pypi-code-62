#!/usr/bin/env python

import argparse
import re
import sys
from datetime import datetime

from clock import talk


def main():
    """
    Convert numeric time to human time and write the result to std out
    """
    parser = argparse.ArgumentParser(description="Convert a numeric time to words")
    parser.add_argument(
        "-t", "--numeric-time", type=str, default=datetime.now().strftime("%H:%M"), help="The time to convert to words"
    )
    args = parser.parse_args()

    if re.search('[a-zA-Z]', args.numeric_time):
        log_and_exit("Error: Provided time [{}] contains non numeric characters".format(args.numeric_time), 1)

    try:
        human_time = talk(args.numeric_time)
        log_and_exit(human_time, 0)
    except ValueError:
        log_and_exit("Error: Numeric time [{}] is not in a valid format".format(args.numeric_time), 1)


def log_and_exit(message, code):
    if code == 0:
        sys.stdout.write(message + "\n")
    else:
        sys.stderr.write(message + "\n")
    sys.stdout.flush()
    sys.exit(code)
