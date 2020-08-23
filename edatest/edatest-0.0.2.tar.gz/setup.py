import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edatest",
    version="0.0.2",
    author="Nicholas Walker",
    author_email="nicholas.walk@gmail.com",
    description="This is a simple package used to run Edabit tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nicholas.walk/edatest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)