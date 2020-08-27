#! /usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='colorcheck',
    version='0.1.0',
    description='Check color contrasts in Web pages',
    url='https://redmine.jpages.eu/projects/colorcheck',
    author='Jérémy Pagès',
    author_email='contact@mail.jpages.eu',
    license='GPL-3.0-or-later',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    packages=find_packages(exclude=('test')),
    python_requires='>=3'
)
