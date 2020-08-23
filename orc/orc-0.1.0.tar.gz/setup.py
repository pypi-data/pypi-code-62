#!/usr/bin/env python
 
import sys

from setuptools import setup

import orc

if sys.version_info[0] < 3:
    sys.exit('Python 3.x is required.')

with open('README.rst') as fp:
    readme = fp.read()

setup(name=orc.__title__,
      version=orc.__version__,
      description=orc.__description__,
      long_description_content_type='text/markdown',
      long_description=readme,
      author=orc.__author__,
      author_email=orc.__author_email__,
      maintainer=orc.__author__,
      maintainer_email=orc.__author_email__,
      url='https://github.com/orange21cn/orc.git',
      packages=[orc.__title__],
      license=orc.__license__,
      python_requires='>3.0',
      classifiers=[]
      )
