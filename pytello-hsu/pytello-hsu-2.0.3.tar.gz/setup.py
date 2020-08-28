import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytello-hsu",
    version="2.0.3",
    author="Alexander Doyle",
    author_email="alexanderthegreat2025@gmail.com",
    description="A package to make it easier to fly your drone in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Suave101/Py-Tello",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
