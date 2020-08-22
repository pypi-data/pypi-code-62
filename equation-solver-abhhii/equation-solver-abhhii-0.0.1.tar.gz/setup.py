import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="equation-solver-abhhii", # Replace with your own username
    version="0.0.1",
    author="Abhishek Singhal",
    author_email="abhhii.cse@gmail.com",
    description="This package allows us to solve linear equations encoded in json form",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url="https://github.com/abhhii/equationSolver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)