import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccalgo",
    version="0.0.1",
    author="Siddharth Marvania, Jenil Mehta",
    author_email="17bit046@nirmauni.ac.in, 17bit048@nirmauni.ac.in",
    description="Using basic algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
