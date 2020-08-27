# -*- coding: utf-8 -*-
from pathlib import Path

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

ext_modules = [
    Extension(
        "libpymath.testModule",
        ["LibPyMath/LibPyMathModules/testModule.c"],
    ),
    Extension(
        "libpymath.test.testModule2",
        ["LibPyMath/LibPyMathModules/testModuleMoreDirs.c"],
    )
]

setup(
    name="libpymath",
    version="0.0.6",
    description="A general purpose Python math module",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Toby Davis",
    author_email="pencilcaseman@gmail.com",
    url="https://www.github.com/pencilcaseman/gpc",
    ext_modules=ext_modules,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
