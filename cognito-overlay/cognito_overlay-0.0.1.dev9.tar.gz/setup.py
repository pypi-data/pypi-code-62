import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="cognito_overlay",
  version="0.0.1-dev09",
  author="Michael Madison",
  author_email="cadetstar@hotmail.com",
  description="Pseudo-application for simplifying authentication with Cognito",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/cadetstar/cognito_overlay",
  packages=setuptools.find_packages(),
  install_requires=[
    'boto3==1.12.35',
    'Flask==1.1.2'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)