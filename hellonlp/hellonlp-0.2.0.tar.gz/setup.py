# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages


with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()
    print(long_description)



setup(
    name="hellonlp",
    version="0.2.0",
    author="Chen Ming",
    author_email="chenming9109@163.com",
    description="NLP tools",
    license="MIT",
    url="https://github.com/hellonlp/hellonlp",
    packages=find_packages(),
    install_requires=[
        'numpy',
        "requests",
        "pygtrie",
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   keywords = 'NLP,Chinese word segementation',
   package_data={'hellonlp':['ChineseWordSegmentation/data/*','ChineseWordSegmentation/dict/*.txt']}
)

