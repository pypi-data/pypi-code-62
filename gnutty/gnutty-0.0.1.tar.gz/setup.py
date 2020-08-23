import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="gnutty",
    version="0.0.1",
    description="Pure Python REST HTTP Server",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/atomicfruitcake/gnutty",
    download_url="https://github.com/atomicfruitcake/gnutty/archive/v0.0.1.tar.gz",
    author="atomicfruitcake",
    license="MIT",
    keywords = ["server", "http", "rest", "api"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["srv"],
    include_package_data=True,
)
