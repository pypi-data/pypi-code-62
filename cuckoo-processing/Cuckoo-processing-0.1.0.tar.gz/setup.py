#!/usr/bin/env python
# Copyright (C) 2020 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - https://cuckoosandbox.org/.
# See the file 'docs/LICENSE' for copying permission.

import setuptools
import sys

if sys.version[0] == "2":
    sys.exit(
        "The latest version of Cuckoo is Python >=3.6 only. Any Cuckoo version "
        "earlier than 3.0.0 supports Python 2."
    )

setuptools.setup(
    name="Cuckoo-processing",
    version="0.1.0",
    author="Stichting Cuckoo Foundation",
    author_email="info@hatching.io",
    packages=setuptools.find_namespace_packages(include=["cuckoo.*"]),
    classifiers=[],
    python_requires=">=3.6",
    url="https://cuckoosandbox.org/",
    license="GPLv3",
    description="Cuckoo Sandbox data processing helpers and modules",
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Cuckoo-common==0.1.0",
        "sflock>=0.3.10, <0.4",
        "protobuf>=3.12.2, <3.13.0"
    ],
)
