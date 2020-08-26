from distutils.core import setup

with open("README.rst", "r") as fh:
  long_description = fh.read()

setup(
  name = 'localspelling',
  packages = ['localspelling'],
  version = '0.8',
  license='MIT', 
  description = 'Translates input between UK and US spelling',
  long_description='''Developed by Fast Data Science, https://fastdatascience.com

Source code at https://github.com/fastdatascience/localspelling

Python library for localising spelling between British and American conventions, conserving case.

Please note this library converts only spelling variants such as US "honour" vs UK "honor".

It does not localise vocabulary such as "pavement" vs "sidewalk" or "aubergine" vs "eggplant".

It also does not localise spellings where there is more than one correct conversion, such as US "program",

which corresponds to both "programme" and "program" in British spelling.''',
  author = 'Thomas Wood',
  #author_email = 'thomas@fastdatascience.com',
  url = 'https://fastdatascience.com',   
  keywords = ['spelling', 'localisation', 'localization', 'uk', 'us', 'british english', 'us english'],
  install_requires=[
          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  include_package_data=True,
)
