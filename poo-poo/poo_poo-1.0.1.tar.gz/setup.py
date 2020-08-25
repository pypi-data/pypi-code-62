import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name="poo_poo",
    version="1.0.1",
    description="see a poopy animation use python -m poo to activate or from poo import poo",
    url="https://pypi.com",
    author="nathblade16",
    author_email="nathblade16@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["poo"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "poo=poo_poo.__main__:main",
        ]
    },
)
