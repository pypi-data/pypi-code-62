import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent


README = (HERE / "README.md").read_text()

setup(
    name="sleekAPI",
    version="1.0.0",
    description="A simple API wrapper for Sleek.to, see GitHub for usage",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRealAkai",
    author="Akai",
    author_email="akai@airmail.cc",
    packages=["sleekAPI"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "sleek=sleek.__init__:main",
        ]
    },
)