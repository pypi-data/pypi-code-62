import setuptools
from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='VFM_IRP_ACSE9',
	author='Nicolas Trinephi',
	author_email='nicolas.trinephi@imperial.ac.uk',
	version='1.0',
	description='Individual MSc Project',
	packages=['VFM_Code'],
	license='xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/acse-2019/irp-acse-nt719/tree/master/Code/'
	)