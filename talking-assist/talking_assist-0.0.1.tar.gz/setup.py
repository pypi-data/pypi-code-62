import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="talking_assist", # Replace with your own username
    version="0.0.1",
    author="shubham jain",
    author_email="jains5833@gmail.com",
    description="Virtual assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shubhamjainjnsb/talking_assist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)