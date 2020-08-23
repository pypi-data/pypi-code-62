import pathlib
import re

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'pyrmq' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_description():
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


PACKAGE = 'pyrmq'
requirements = ["aioredis>=1.3,<1.4", "loguru~=0.5"]

setup(
    name='python-rmq',
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/Forden/pyrmq',
    license='MIT',
    author='Forden',
    author_email='forden@forden.me',
    description='Redis based message queue',
    long_description=get_description(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={
        'fast': [
            'uvloop>=0.14.0,<0.15.0',
        ]
    }
)
