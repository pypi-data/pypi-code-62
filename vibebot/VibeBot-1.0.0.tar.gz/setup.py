#!/usr/bin/env python3

""" Setup file for VibeBot package.
"""
import sys

from setuptools import setup, find_packages
from pkg_resources import VersionConflict, require

import VibeBot

try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)


if __name__ == "__main__":
    setup(
        name=VibeBot.__title__,
        version=VibeBot.__version__,
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=["tests"]),
        install_requires=[
            "certifi==2020.6.20",
            "chardet==3.0.4",
            "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "flask==1.1.2",
            "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "importlib-metadata==1.7.0; python_version < '3.8'",
            "itsdangerous==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "jinja2==2.11.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "markdown==3.2.2",
            "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "requests==2.24.0",
            "urllib3==1.25.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
            "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "zipp==3.1.0; python_version >= '3.6'",
        ],
        include_package_data=True,
        zip_safe=False,
        # Uncomment if needed
        # entry_points={"console_scripts": ["VibeBot=VibeBot.__main__:main"]},
        author=VibeBot.__author__,
        author_email=VibeBot.__author_email__,
        description=VibeBot.__description__,
        license=VibeBot.__license__,
        keywords=VibeBot.__keywords__,
        url=VibeBot.__url__,
        project_urls=VibeBot.__project_urls__,
    )
