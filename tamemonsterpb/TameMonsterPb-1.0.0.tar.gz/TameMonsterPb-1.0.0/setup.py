import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = "TameMonsterPb",
  version = "1.0.0",
  author = "sinerwr",
  author_email = "sinerwr@gmail.com",
  url = "https://git.iflyos.cn/SRE/TameMonster/TameMonsterPb",
  description = "tm protobuf",
  long_description = long_description,
  license = "MIT Licence",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  packages = setuptools.find_packages()

)
