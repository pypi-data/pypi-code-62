import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydyimport",
    version="0.0.1-alpha.1",
    author="thisLight",
    author_email="l1589002388@gmail.com",
    description=
    "Dynamically import python file to aviod mess when you are using a different structure from python suggested.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thislight/pydyimport",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
