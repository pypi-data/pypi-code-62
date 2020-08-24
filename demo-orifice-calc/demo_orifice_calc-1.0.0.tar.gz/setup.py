import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="demo_orifice_calc",
    version="1.0.0",
    description="Demonstration of an orifice calculation module",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Darren Hewett",
    author_email="",
    license="MIT",
    py_modules=['demo_orifice_calc'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["scipy", "math"],
)
