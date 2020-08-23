import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ystockQuery", # Replace with your own username
    version="0.1.0",
    author="Alan Cheng",
    author_email="alancslhkse@gmail.com",
    description="A Yahoo Finance wrapper for stock quotes and historical data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alancslhk/ystockQuery",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)