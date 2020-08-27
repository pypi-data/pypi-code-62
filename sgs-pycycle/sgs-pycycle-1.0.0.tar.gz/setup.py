# -*- coding: utf-8 -*-

import setuptools

import sgs_pycycle


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='sgs-pycycle',
    version=sgs_pycycle.__version__,
    author=sgs_pycycle.__author__,
    author_email='sgs@pichove.org',
    description='A Python client and object-mapper for the Oslo Bysykkel API',
    license=sgs_pycycle.__license__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sgs-test/sgs-pycycle',
    packages=setuptools.find_packages(),
    exclude_package_data={'': ['.gitignore']},
    entry_points={
        'console_scripts': [
            'sgs_pycycle=sgs_pycycle.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Topic :: Internet :: WWW/HTTP'
    ],
    keywords='oslo bikes bicycle api',
    project_urls={
        'Bug Reports': 'https://github.com/sgs-test/sgs-pycycle/issues',
        'Source': 'https://github.com/sgs-test/sgs-pycycle'
    },
    python_requires='>=3.6',
)
