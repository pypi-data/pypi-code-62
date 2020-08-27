import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythematics", 
    version="1.1.1",
    author="Leonidios Megalopoutsas",
    author_email="programertv633@example.com",
    description="A math library that extends the built-in one with complex function domains and linear algebra operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Greece4ever/pythematics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
