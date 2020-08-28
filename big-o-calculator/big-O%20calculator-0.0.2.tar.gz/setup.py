from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='big-O calculator',
      version='0.0.2',
      description='A calculator to predict big-O of sorting functions',
      url='https://github.com/Alfex4936',
      author='Seok Won',
      author_email='tjrdnjs33936@gmail.com',
      license='MIT',
      packages=['bigO'],
	  long_description=long_description,
	  long_description_content_type="text/markdown",
	  python_requires  = '>=3',
      include_package_data=True,
	  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
	  install_requires=[
        'win10toast'
      ],
      zip_safe=False)
