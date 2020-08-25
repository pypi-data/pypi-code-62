import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bric-layer",
    version="0.0.1",
    author="G B",
    description="Layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bankova-gabriella/layer/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

# python setup.py sdist & twine upload --repository pypi dist/*
