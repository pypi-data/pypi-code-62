import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-ksgsarma", # Replace with your own username
    version="0.0.1",
    author="ksgsarma",
    author_email="ksgsarma5@gmail.com",
    description="A small housie ticket generation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ksgsarma/Housie_PyPi.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)