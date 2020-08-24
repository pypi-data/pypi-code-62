#!/usr/bin/env python3
# Json library support hex escape.
from os.path import join, dirname
from setuptools import setup, find_packages


VERSION = (0, 0, 5)
__version__ = VERSION
__versionstr__ = "0.0.5"


with open(join(dirname(__file__), "README.md")) as f:
    long_description = f.read().strip()


install_requires = [
    #"numpy",
    #"pandas",
]


setup(
    name="hexson",
    description="Json library which enable user to parse and dump data with hex escape",
    license="Apache-2.0",
    url="https://github.com/wonderqs/hexson",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__versionstr__,
    author="ManchurianClassmate",
    author_email="i@listenwhat.com",
    maintainer="ManchurianClassmate",
    maintainer_email="i@listenwhat.com",
    packages=find_packages(where="."),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    install_requires=install_requires
)
