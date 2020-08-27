import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api-estcube-helpers", # Replace with your own username
    version="0.0.1",
    author="Umesh .A Bhat",
    author_email="umesh.bhat@estcube.eu",
    description="Helper functions for ESTCube Mission Control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/estcube/api-estcube-helpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)