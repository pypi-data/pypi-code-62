from setuptools import setup
from setuptools import find_packages

from A4Shape import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="A4Shape", # Replace with your own username
    version=__version__,
    author="Programmer",
    author_email="Anonymousfromthedigitalworld@gmail.com",
    description="Shapes And Animations For Linux Python Tools..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Black7unter-X/A4Shape",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ]
)

