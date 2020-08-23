from distutils.core import setup

VERSION = "0.1.5"

setup(
    name="gitlab-emulator",
    version=VERSION,
    description="Run a subset of .gitlab-ci.yml jobs locally",
    author="Ian Norton",
    author_email="inorton@gmail.com",
    url="https://gitlab.com/cunity/gitlab-emulator",
    packages=["gitlabemu"],
    scripts=["locallab.py"],
    install_requires=["pyyaml>=3.13", "pytest>=5.1", "pytest-mock>=3.3.0"],
    platforms=["any"],
    license="License :: OSI Approved :: MIT License",
    long_description="Run a subset of .gitlab-ci.yml jobs locally using docker"
)
