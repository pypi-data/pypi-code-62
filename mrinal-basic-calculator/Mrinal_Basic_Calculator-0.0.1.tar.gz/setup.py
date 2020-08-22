from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
] 

setup(
    name = 'Mrinal_Basic_Calculator',
    version = '0.0.1',
    description = 'A very elementary calculator',
    Long_description=open('Readme.txt').read()+ '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author = 'Mrinal M',
    author_email= 'mrinal.m.iiitb@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)