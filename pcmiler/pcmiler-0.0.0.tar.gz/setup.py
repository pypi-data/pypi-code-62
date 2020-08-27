from setuptools import setup, find_packages
from pcmiler import __version__


long_description = ''
with open('./README.md') as f:
    long_description = f.read()

install_requires = []
with open('./requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='pcmiler',
    version=__version__,
    description='pcmiler wrapper python package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nfi-engineering/pcmiler',
    author='Chris Pryer',
    author_email='chris.pryer@nfiindustries.com',
    license='PUBLIC',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points ={ 
            'console_scripts': [ 
                'pcmiler = pcmiler.main:main'
            ] 
        },
    zip_safe=False)