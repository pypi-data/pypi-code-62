from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Basic-Calculator 2.0',
  version='0.0.1',
  description='My First Python Package',
  long_description=open('Readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Neelansh Agarwal',
  author_email='py4e@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Calculator', 
  packages=find_packages(),
  install_requires=[''] 
)