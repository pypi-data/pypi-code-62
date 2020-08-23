
from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from subprocess import check_call


class PostDevelopCommand(develop):
  """Post-installation for development mode."""

  def run(self):
    raise Exception("This is not the python-logging-utils you are looking for /jediwave")
    develop.run(self)


class PostInstallCommand(install):
  """Post-installation for installation mode."""

  def run(self):
    raise Exception("This is not the python-logging-utils you are looking for /jediwave")
    install.run(self)


class EggInfoCommand(egg_info):
  """Post-installation for installation mode."""

  def run(self):
    print("This is not the python-logging-utils you are looking for /jediwave")
    egg_info.run(self)


setup(
    name='python-security-utils',
    packages=['python-security-utils'],  # this must be the same as the name above
    version='0.0.1',
    description='The wrong python-security-utils library.',
    author='appsec @ tempus',
    author_email='mark.collao@tempus.com',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        'egg_info': EggInfoCommand,
    },  # I'll explain this in a second
    entry_points={
        'console_scripts': [
            'python-security-utils=python_security_utils.cli:cli',
        ]
    }
)

