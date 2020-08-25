# @Time    : 2020/8/24 20:24
# @Author  : alita
# File     : setup.py

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="DataDocking",
  version="0.0.3",
  author="alita",
  author_email="1906321518@qq.com",
  description="Data Docking package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/AlitaIcon/DataDocking",
  packages=setuptools.find_packages(include=['DataDocking', 'DataDocking.*']),
  # package_dir={'': 'DataDocking'},  # 必填
  license='MIT',
  include_package_data=True,
  install_requires=[
      'records>=0.5.3'
  ],
  python_requires='>=3.6',
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  project_urls={
    'Documentation': 'https://github.com/AlitaIcon/DataDocking',
    'Source': 'https://pypi.org/project/DataDocking/',
  },
)