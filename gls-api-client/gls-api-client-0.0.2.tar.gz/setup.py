import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gls-api-client",
    version="0.0.2",
    author="Steven Athouel",
    author_email="sathouel@gmail.com",
    description="A simple api client for GLS carrier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sathouel/gls_api_client.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)