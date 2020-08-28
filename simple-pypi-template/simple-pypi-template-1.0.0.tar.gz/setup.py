import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-pypi-template",
    version="1.0.0",
    author="Ramón Invarato Menéndez",
    author_email="r.invarato@gmail.com",
    description="Template and instructions to create a Python module and upload to PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Invarato/simple_pypi_template_project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
