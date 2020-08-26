from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='decap',
  version='0.0.1',
  description='A simple function for decapitalizing text.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Peter Kyle',
  author_email='peterdooga@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='decap decapitalize', 
  packages=find_packages(),
  install_requires=[''] 
)
