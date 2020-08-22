#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for package install
"""
import os
from setuptools import setup
import versioneer

################################################################################

# Note: setup.cfg is set up to only recognise tags starting with v

# git describe --tags # gets the current tag
# git tag v0.0.01 # update the tag to something, e.g. v0.0.01
# git push origin --tags # push update to branch

# conda activate python_env
# python3 -m pip install --user --upgrade setuptools wheel
# rm -rf build;rm -rf dist;rm -rf *.info;rm -rf *.egg-info
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*

################################################################################

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

def read_text(file_name: str):
    return open(file_name).read()

################################################################################

def setup_package():
    """
    Function to manage setup procedures.
    """

    setup(
        name="lind",
        packages=["lind"],
        version=versioneer.get_version(),

        author="James Montgomery",
        author_email="jamesoneillmontgomery@gmail.com",
        description="Package for implementing bayesian deep conjugate models in python.",
        long_description=read_text("README.md"),
        long_description_content_type="text/markdown",
        license=read_text("LICENSE.md"),

        python_requires=">=3.6",
        platforms='any',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],

        install_requires=parse_requirements("requirements.txt"),
        extras_require={
            "tests": parse_requirements("requirements_test.txt")
        },
        cmdclass = versioneer.get_cmdclass(),
        setup_requires=['wheel']
    )

if __name__ == "__main__":
    setup_package()
