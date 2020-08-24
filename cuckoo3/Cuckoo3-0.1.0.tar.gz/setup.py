#!/usr/bin/env python
# Copyright (C) 2020 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - https://cuckoosandbox.org/.
# See the file 'docs/LICENSE' for copying permission.

import setuptools
import sys

if sys.version[0] == "2":
    sys.exit(
        "The latest version of Cuckoo is Python >=3.6 only. Any Cuckoo version"
        " earlier than 3.0.0 supports Python 2."
    )

setuptools.setup(
    name="Cuckoo3",
    version="0.1.0",
    author="Stichting Cuckoo Foundation",
    author_email="info@hatching.io",
    packages=setuptools.find_namespace_packages(include=["cuckoo.*"]),
    classifiers=[],
    keywords="",
    python_requires=">=3.6",
    url="https://cuckoosandbox.org/",
    license="GPLv3",
    description="Automated Malware Analysis System",
    long_description=open("README.rst", "r").read(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "cuckoo = cuckoo.main:main",
        ],
    },
    install_requires=[
        "Cuckoo-common==0.1.0",
        "Cuckoo-processing==0.1.0",
        "Cuckoo-machineries==0.1.0",
        "sflock>=0.3.10, <0.4"
    ]
)
