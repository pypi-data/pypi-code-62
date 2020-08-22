from __future__ import print_function
from setuptools import setup

setup(
    name="hermes-subscribe",
    version="1.0",
    author="zcq100",
    author_email="zcq100@gmail.com",
    description="hermes goods update notification",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache License",
    url="https://github.com/zcq100/hermes-subscribe",
    # packages=['hermes'],
    install_requires=[
        'prettytable',
    ],
    
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

