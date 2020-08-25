import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toshi", # Replace with your own username
    version="0.0.3",
    author="Athul Mathew Konoor",
    author_email="athulmathewkonoor@gmail.com",
    description="A package to install machine learning, deep learning packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toshihiroryuu/Hammurabi_pip_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)