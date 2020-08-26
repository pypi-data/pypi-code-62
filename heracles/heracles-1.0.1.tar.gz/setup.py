import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

reqs = parse_requirements('requirements.txt')
if sys.platform == "win32":
    reqs.append('pywin32')

setuptools.setup(
    name="heracles",
    version="1.0.1",
    author="Luarle Sousa",
    author_email="luarle.sousa@sidia.com",
    description="Heracles - GUI helper for PreSMC ATLAS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luarlelima/heracles",
    py_modules=["heracles", ""],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'heracles = heracles:main',
            ],
        },
    install_requires=reqs,
    python_requires='>=3.7',
)
