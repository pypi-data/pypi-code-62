import io
import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ["google-cloud-iam"]

setuptools.setup(
    name="gcp-oidc",
    version="0.0.10",
    author="Total Wine",
    author_email="crsintegrations@totalwine.com",
    description="Generate OIDC tokens for GCP Service accounts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)