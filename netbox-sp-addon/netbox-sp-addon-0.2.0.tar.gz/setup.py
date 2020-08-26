from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='netbox-sp-addon',
    version='0.2.0',
    description='Adds some functions used by scanplus GmbH',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ScanPlusGmbH/netbox-sp-addon',
    author='Tobias Genannt',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
)

