from setuptools import setup, find_packages
from distutils.extension import Extension

version = '0.1.6'


setup(name='wsmocky',
      version=version,
      description="Create dynamic mock server with wsdl file.",
      long_description="""Create dynamic mock server with wsdl file.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='webservice mock',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger/wsmocky',
      license='MIT',
      packages=['wsmocky'],
      zip_safe=True,
      install_requires=[
          "tornado",
          "lxml",
          "click",
          "requests"
      ],
      entry_points={
        'console_scripts': ['wsmocky=wsmocky.wsmocky:main'],
      },
      )
