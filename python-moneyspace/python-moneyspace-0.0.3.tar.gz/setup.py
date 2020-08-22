# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='python-moneyspace',
    version='0.0.3',
    author=u'Jon Combe',
    author_email='jon@salebox.io',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    url='https://github.com/joncombe/python-moneyspace',
    license='BSD licence, see LICENCE file',
    description='Python class to connect with moneyspace.net payment gateway',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
