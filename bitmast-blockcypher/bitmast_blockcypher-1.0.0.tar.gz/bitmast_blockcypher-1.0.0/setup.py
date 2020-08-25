import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README.md file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bitmast_blockcypher",
    version="1.0.0",
    description="Python wrapper for accessing BlockCypher API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bitmast Digital Services",
    author_email="frier17@a17s.co.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bitmast_blockcypher"],
    include_package_data=True,
    install_requires=["bitcoinlib", "blockcypher"]
)
