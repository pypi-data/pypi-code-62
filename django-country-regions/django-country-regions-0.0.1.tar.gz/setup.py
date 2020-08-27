from setuptools import setup, find_packages
import shutil
import sys
import os
import os.path


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-country-regions',
    version='0.0.1',
    description='C',
    author='afranck64',
    #author_email='',
    url='https://github.com/afranck64/django-country-regions',
    packages=['country_regions'],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='django countries regions',
    install_requires=[
        'django-autoslug>=1.9.8',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)