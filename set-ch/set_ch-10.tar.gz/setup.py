import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="set_ch",
    version="10",
    author="gmj021",
    author_email="13002152679@163.com",
    description="a package can save the problem of matolplib",
    install_requires=['matplotlib'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmj021/set_ch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
