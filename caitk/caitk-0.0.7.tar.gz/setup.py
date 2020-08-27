# -*- coding: utf-8 -*-
# Copyright (C) 2020 Caitum Technologies

from setuptools import setup, find_packages


DESCRIPTION="""
Caitum Artificial Intelligence Toolkit
======================================

License
-------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""


setup(
    name='caitk',
    version='0.0.7',
    description='Caitum Artificial Intelligence Toolkit',
    license='GPL-3.0-only',

    long_description=DESCRIPTION,
    long_description_content_type='text/x-rst',
    author='Caitum Technologies',
    author_email='devel@caitum.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='caitum artificial-intelligence',

    url='https://github.com/caitum/caitk',
    project_urls={
        'Issues': 'https://github.com/caitum/caitk/issues'
    },

    packages=find_packages(exclude=['tests*']),
    install_requires=[],

    include_package_data=True,
    zip_safe=True
)
