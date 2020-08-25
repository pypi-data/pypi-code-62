#!/usr/bin/env python3
# Setup python package - python setup.py sdist

from setuptools import setup

setup(
    name='randstr-random',
    version='1.1.1',
    py_modules=['randstr'],
    license='MIT',
    description='A Python package for generating strings with random characters built on top of the random module.',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/randstr-random',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux']
)