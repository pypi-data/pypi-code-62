from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(name='pylol',
	version='1.0.12',
	description="A Module to get basic modules like the Time Module and Math Modules and combine them into one so you don't need to import so many modules!",
	long_description=readme(),
	long_description_content_type='text/markdown',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent'
	],
	url='https://gist.github.com/BXRSRUDIOS',
	author="BXRCODES",
	author_email="19braja@rgshw.com",
	keywords='core package',
	license='MIT',
	packages=['Pylol'],
	include_package_data=True,
	zip_safe=False)