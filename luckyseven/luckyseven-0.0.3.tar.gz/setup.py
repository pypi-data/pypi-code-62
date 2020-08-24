from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="luckyseven",
    version="0.0.3",
    author="Matías Barrios Núñez",
    author_email="matias.barriosn@gmail.com",
    description="Lightweitght CSPRNG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matiasbn/luckyseven",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
