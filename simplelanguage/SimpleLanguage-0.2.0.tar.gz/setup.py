import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleLanguage",
    version="0.2.0",
    author="Acuf5928",
    author_email="alberto.cuffaro@hotmail.it",
    description="Multi language tool for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Acuf5928/SimpleLanguage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)