#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['bankfind', 'bankfind.metadata']

package_data = \
{'': ['*']}

install_requires = \
['requests == 2.24.0', 'pandas>=0.24']

extras_require = \
{'doc': ['mkdocs-material', 'pymdown-extensions'],
 'test': ['pytest', 'coverage', 'pytest-cov']}

setup(name='bankfind',
      version='0.0.1',
      description="Python interface to the FDIC's API for publically available bank data",
      author='Doug Guthrie',
      author_email='douglas.p.guthrie@gmail.com',
      url='https://github.com/dpguthrie/bankfind',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
     )
