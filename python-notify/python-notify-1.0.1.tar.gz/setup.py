import pathlib
from setuptools import setup, find_packages


readme_file = pathlib.Path(__file__).parent / 'README.md'
with readme_file.open(encoding='utf-8') as stream:
    readme_content = stream.read()

setup(
    name='python-notify',
    version='1.0.1',
    author='DanilaKorobkov',
    author_email='korobkov.danila.yurevich@gmail.com',
    url='https://github.com/DanilaKorobkov/python-notify',
    description='Implementation of observer design pattern in python3',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    keywords='observer signal slots notify publish subscriber notifiable_property',
    packages=find_packages(),
)
