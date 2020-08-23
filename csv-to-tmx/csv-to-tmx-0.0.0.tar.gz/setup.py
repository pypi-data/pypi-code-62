from setuptools import setup
from os.path import abspath, dirname, join

root_dir = abspath(dirname(__file__))

with open(join(root_dir, "README.md")) as f:
    long_description = f.read()

setup(
    name = 'csv-to-tmx',
    packages = ['csv_to_tmx'],
    package_dir = {'csv_to_tmx': 'csv_to_tmx'},
    version = '0.0.0',
    description = 'Creates a tmx file from a csv',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Victoria Mak',
    author_email = 'victoria@mak4lab.com',
    url = 'https://github.com/mak4lab/csv-to-tmx',
    download_url = 'https://github.com/mak4lab/csv-to-tmx/tarball/download',
    keywords = ['parallel corpus', 'machine translation', 'nmt', 'csv', 'tmx', 'translation memory', 'mt', 'sentence alignment'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ]
)
