# Copyright 2019 Splunk Inc. All rights reserved.
"""Helper module to verify runtime environment"""

# Python Standard Libraries
import sys


def validate_python_version():
    """To validate if the python version meet the requirement of AppInspect CLI"""
    major, minor, _, _, _ = sys.version_info
    version_detected = str(major) + "." + str(minor)

    if (major, minor) != (3, 7):
        python_version_message = (
            "Python version {} was detected. Splunk AppInspect only supports Python 3.7"
        ).format(version_detected)
        sys.exit(python_version_message)
