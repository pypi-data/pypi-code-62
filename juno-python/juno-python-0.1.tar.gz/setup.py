from setuptools import setup, find_packages


__description__ = "Juno Python"
__long_description__ = "Python library for Juno API"

__author__ = "Manaia Junior"
__author_email__ = "manaiajr.23@gmail.com"

setup(
    name="juno-python",
    version="0.1",
    url="https://github.com/mjr/juno-python",
    author=__author__,
    author_email=__author_email__,
    license="MIT",
    description=__description__,
    long_description=__long_description__,
    keywords="Payment, Juno",
    packages=find_packages(),
    install_requires=["requests>=2.24.0"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
