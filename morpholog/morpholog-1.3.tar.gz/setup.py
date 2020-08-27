import os
import setuptools

with open('C:\projects\morpholog\README.txt') as readme_file:
    README = readme_file.read()

setuptools.setup(
     name='morpholog',  
     version='1.3',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="Morpholog provides many methods for working with morphological structure of russian word",
     include_package_data=True,
     long_description=README,
     keywords=['tokenizer', 'morphemes', 'NLP', 'russian'],
     url="https://github.com/constantin50/morphological_tokenizer",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
