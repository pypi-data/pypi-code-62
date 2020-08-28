#!/usr/bin/env python


#from distutils.core import setup
from setuptools import setup

with open("README.rst") as file_object:
    description = file_object.read()

setup(name='mapykoB',
      version='0.0.3',
      author='Andzl',
      author_email='andzlhub@gmail.com',
      url='https://github.com/octoandzl/mapykoB',
      long_description=description,
      description="Package for sequence modeling with Andrei Markov's models",
      license="MIT",
      packages=['mapykoB', 'mapykoB.discreet'],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    data_files=[("", ["LICENSE"])]
      )
