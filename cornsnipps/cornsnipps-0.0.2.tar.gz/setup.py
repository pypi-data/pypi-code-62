from setuptools import setup, find_packages
from cornsnipps import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='cornsnipps',
    version=__version__,
    description='A set of useful objects, functions and snippets',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/akonieczny/cornsnipps',
    author='Adam Konieczny',
    packages=find_packages(include=['cornsnipps', 'cornsnipps.*']),
    python_requires='>=3.5, <4',
    license='BSD 3-Clause License',
    zip_safe=False,
    project_urls={
        'Issues': 'https://github.com/akonieczny/cornsnipps/issues',
        'Source': 'https://github.com/akonieczny/cornsnipps',
    },
)
