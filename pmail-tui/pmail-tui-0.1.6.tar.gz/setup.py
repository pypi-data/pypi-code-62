#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

# ---> Imports

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
import pmail 

# <---

# ---> Setup

# Package meta-data.
NAME = 'pmail-tui'
DESCRIPTION = 'TUI client for gmail'
URL = 'https://github.com/lt20kmph/pmail'
EMAIL = 'o.g.sargent@gmail.com'
AUTHOR = 'Oliver Sargent'
REQUIRES_PYTHON = '>=3.6.0'
# VERSION = '0.1.3'
VERSION = pmail.__version__

# What packages are required for this module to be executed?
REQUIRED = [
  'sqlalchemy',
  'google-api-python-client>=1.10.0',
  'google-auth-httplib2',
  'google-auth-oauthlib'
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['pmail'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Email Clients (MUA)',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

# <---

# ---> Old functions
'''
def setSendAs(email, name):
  service = mkService()
  sendAsResource = {'sendAsEmail': email,
                    'replyToAddress': email,
                    'displayName': name}
  response = service.users().settings().sendAs().update(userId = 'me',
          sendAsEmail = email,
          body=sendAsResource).execute()
  return response

def listSendAs():
  service = mkService()
  response = service.users().settings().sendAs().list(userId = 'me'
          ).execute()
  return response


if __name__ == '__main__':
    emailAddress = (s.query(UserInfo)[0]).emailAddress
    logger.info('Attempting to set send as name: {} for {}'.format(
        getName(emailAddress),
        emailAddress
        ))
    print(setSendAs(emailAddress, getName(emailAddress)))
    print(listSendAs())
'''
# <---

"""
vim:foldmethod=marker foldmarker=--->,<---
"""
