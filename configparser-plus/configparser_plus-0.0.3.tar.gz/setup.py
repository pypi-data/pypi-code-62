import setuptools
import sys
if sys.version_info[0] < 3:
    with open("README.md", "r") as fh:
        long_description = fh.read()
if sys.version_info[0] >= 3:
    with open("README.md", encoding='utf-8') as fh:
        long_description = fh.read()

setuptools.setup(
    name="configparser_plus",
    version="0.0.3",
    author="Leviathan-litan",
    author_email="leviathan_litan@163.com",
    description="The advance version of origin configparser.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/leviathan-litan/python_config_file_plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Development Status :: 5 - Production/Stable",
    ],
)