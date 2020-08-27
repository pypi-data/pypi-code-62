#!/usr/bin/env python3
# coding=utf-8
"""Setup for module jsontextmc"""
import setuptools

from jsontextmc import constants

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name=constants.PROJECT.lower(),
    version=constants.VERSION,
    author="whoatemybutte7",
    author_email="4616947-whoatemybutte7@users.noreply.gitlab.com",
    description=constants.DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/whoatemybutte7/jsontextmc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Localization",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Games/Entertainment :: Simulation"
    ],
    python_requires='>=3.6',
)
