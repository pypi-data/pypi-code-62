# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages
from luaproject.manager import get_version

import package_clean_name

here = os.path.abspath(os.path.dirname(__file__))

rockspec_filename = os.path.abspath(os.path.join(os.path.dirname(package_clean_name.__file__), "./src/.rockspec"))
with open(rockspec_filename, "r", encoding="utf-8") as fobj:
    version = get_version(fobj.read()).replace("-", ".")
print("rockspec_filename=", rockspec_filename)
print("version=", version)

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="package-name",
    version=version,
    description="package-name description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YOUR NAME HERE",
    author_email="YOUR EMAIL HERE",
    url="YOUR PROJECT URL HERE, OPTIONAL.",
    license="YOU LICENSE NAME HERE",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=[],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["manage_package_clean_name", "package_clean_name"],
    entry_points={
        "console_scripts": [
            "manage-package-name = manage_package_clean_name:manager",
        ]
    },
    zip_safe=False,
    include_package_data=True,
)
