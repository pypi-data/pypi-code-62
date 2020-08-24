#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.7"

__all__ = ()

from pathlib import Path
from setuptools import setup, find_packages
from shutil import rmtree

BUILD_DIRS = (
    'api_bridge.egg-info',
    'build',
    'dist'
)


if __name__ == '__main__':
    for d in BUILD_DIRS:
        path = Path(d)
        if path.exists() and path.is_dir():
            print(f'Deleting {path}...')
            rmtree(d)

    setup(
        name='api_bridge',
        version=__version__,
        packages=find_packages(),
        url='https://github.com/robin-weiland/APIBridge',
        license='MIT',
        author=__author__,
        author_email='robin.weiland@gmx.de',
        description='Joining json API calls together',
        long_description=Path('README.md').read_text(),
        long_description_content_type='text/markdown',
        keywords=['api', 'json', 'web'],
        python_requires='>=3.6',  # due to __class_getitem__  see PEP560
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development',  # sort of
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Operating System :: OS Independent',
        ],
        requires=[line.split('=')[0].rstrip('~<>=')
                  for line in Path('requirements.txt').read_text().splitlines()
                  if not (line.startswith('#') or line == '' or line == '\n' or line.endswith('###'))]
    )
