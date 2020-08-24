from setuptools import setup, find_packages
from pyweb import __version__ as version
# http://blog.codekills.net/2011/07/15/lies,-more-lies-and-python-packaging-documentation-on--package_data-/

# read the contents of your README file
with open('README.md') as f:
    long_description = f.read()


setup(
    name='lob-pyweb',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    package_dir={'pyweb': "pyweb"},
    packages=find_packages(include=["pyweb*"]),
    package_data={'pyweb': ['pyweb/blueprints/**/templates/**', 'pyweb/blueprints/**/static/**']},
    include_package_data=True,
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    url='https://github.com/lobnek/pyweb',
    description='',
    install_requires=['flask>=1.1.2', 'flask-caching>=1.9.0', 'waitress>=1.4.4', 'dash>=1.12.0', 'dash-daq>=0.5.0', 'flask-mongoengine>=0.9.5', 'whitenoise>=5.1.0', 'dnspython>=1.16.0', 'flask-bootstrap>=3.3.7.1'],
    license="MIT"
)
