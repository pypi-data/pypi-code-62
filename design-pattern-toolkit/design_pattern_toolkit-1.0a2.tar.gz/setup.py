import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='design_pattern_toolkit',
      version='1.0a2',
      description='Collection of design patterns implemented in Python',
      url='https://gitlab.com/frier17/toolkit.git',
      author='https://gitlab.com/frier17/',
      author_email='frier17@a17s.co.uk',
      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      packages=['toolkit', 'toolkit/behaviour', 'toolkit/creation', 'toolkit/tests'],
      include_package_data=True
      )
