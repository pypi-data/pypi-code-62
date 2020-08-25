import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasode_mei_kaun_tha", # Replace with your own username
    version="0.0.4",
    author="imzain448",
    author_email="ahmadzain.448@gmail.com",
    description="the mystery unveiled",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imZain448/dummy_pypi_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['matplotlib'],
    include_package_data=True
)