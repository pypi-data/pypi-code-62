import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moodys_custom_operations",
    version="0.0.3",
    author="Subhajit Ganguli",
    author_email="subhajit.ganguli-non-empl@moodys.com",
    description="Some useful arithmetic and boolean operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.moodys.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)