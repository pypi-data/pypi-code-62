#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests', 'watchdog']

setup_requirements = ['setuptools_scm']

test_requirements = ['pytest']

setup(
    author="Dominik Stańczak",
    author_email='stanczakdominik@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Script to automatically upload new files appearing in a directory to sc2replaystats.",
    entry_points={
        'console_scripts': [
            'sc2replaystats_uploader=sc2replaystats_uploader.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='sc2replaystats_uploader',
    name='sc2replaystats_uploader',
    packages=find_packages(include=['sc2replaystats_uploader', 'sc2replaystats_uploader.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/stanczakdominik/sc2replaystats_uploader',
    zip_safe=False,
)
