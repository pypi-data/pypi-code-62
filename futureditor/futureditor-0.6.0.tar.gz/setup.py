import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="futureditor",
    version="0.6.0",
    description="code editor",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjaymarison/futureditor",
    author="SanjayMarison",
    author_email="sanjaymarison@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["futureditor"],
    include_package_data=True,
    install_requires=[],
    scripts=['bin/future-editor.py'],
    entry_points={
        "console_scripts": [
            "SanjayMarison=futureditor.__main__:main",
        ]
    },
)
