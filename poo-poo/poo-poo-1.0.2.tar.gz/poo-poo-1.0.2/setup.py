import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name="poo-poo",
    version="1.0.2",
    description="see a poopy animation use python -m poo to activate import poo-poo",
    url="https://pypi.com",
    author="nathblade16",
    author_email="nathblade16@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_reqyires='>=3.6',
)
