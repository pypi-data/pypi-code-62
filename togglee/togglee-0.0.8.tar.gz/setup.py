import os
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements_prod.txt') as f:
    required = f.read().splitlines()

setup(
    name='togglee',
    version=f'0.0.{os.getenv("GITHUB_RUN_NUMBER", "1-SNAPSHOT")}',
    description='Simple toggles for python from a url reference',
    long_description=readme,
    author='kanekotic',
    author_email='me@kanekotic.com',
    url='https://github.com/togglee/togglee-python',
    install_requires=required,
    license=license,
    packages=find_packages()
)
