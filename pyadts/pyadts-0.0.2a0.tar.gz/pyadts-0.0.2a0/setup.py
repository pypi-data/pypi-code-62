import os

from setuptools import setup


def __parse_requirements(file_name):
    with open(file_name, 'r') as f:
        line_striped = (line.strip() for line in f.readlines())
    requirements = [line for line in line_striped if line and not line.startswith('#')]
    # requirements.append(__check_pytorch())
    return requirements


# Get description from README
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyadts',
    author='Xiao Qinfeng',
    author_email='larryshaw0079@live.com',
    description='A python package for time series anomaly detection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.2a',
    packages=[],
    scripts=[],
    install_requirements=__parse_requirements('requirements.txt'),
    # cmdclass={'install': __PostInstallMoveFile},
    url='https://github.com/larryshaw0079/PyADT',
    python_requires=">=3.5",
    license='GPL-3.0 License'
)
