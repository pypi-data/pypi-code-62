import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="3ptest",
    version="1.0.0",
    description="3P Test Package",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["3ptest"],
    entry_points={
        "console_scripts": [
            "3ptest=3ptest.__main__:main",
        ]
    },
)
