#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from os import path
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

try:
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements

from setuptools import find_packages, setup


def get_requirements(requirements_file):
    """Use pip to parse requirements file."""
    requirements = []
    dependencies = []
    if path.isfile(requirements_file):
        for req in parse_requirements(requirements_file, session="hack"):
            try:
                if req.match_markers():
                    requirements.append(str(req.req))
                    if req.link:
                        dependencies.append(str(req.link))
            except AttributeError:
                requirements.append(req.requirement)
    return requirements, dependencies

if __name__ == "__main__":
    HERE = path.abspath(path.dirname(__file__))
    INSTALL_REQUIRES = get_requirements(path.join(HERE, "requirements.txt"))

    with open(path.join(HERE, "README.rst")) as readme:
        LONG_DESCRIPTION = readme.read()

    setup(
        name='mbizmomo',
        description='Python wrapper for the MTN MoMo API.',
        long_description=LONG_DESCRIPTION,
        license='MIT',
        #version='1.0.0',
        author='Amonak',
        url='https://github.com/amonak/mbizmomo',
        author_email='amonak@alphamonak.com',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Utilities',
        ],
        keywords=[
            'MoMo API', 'MoMo API Python Wrapper', 'MoMo API Python',
        ],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
        use_scm_version=True,
        python_requires=">=3.4",
        setup_requires=["setuptools_scm", "pytest-runner", "pytest-cov"],
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        extras_require={'test': ['pytest', 'pytest-watch', 'tox',
                                 'pytest-cov',
                                 'pytest-pep8',
                                 'pytest-cov',
                                 'pytest-sugar',
                                 'mock', 
                                 'pytest-runner',
                                 'pytest-instafail',
                                 'pytest-bdd'], "dev": ["semver"]},
        entry_points={
            'console_scripts': [
                 'mbizmomo = mbizmomo.cli:main',
            ]
        },
    )
