import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="RemotePyLib",
    version="1.0.0",
    author="Nalin Studios",
    author_email="nalinangrish2005@gmail.com",
    description="A package to import libraries remotely.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nalinstudios.herokuapp.com/remotepylib/source",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'importlib',
        'bs4'
    ],
    python_requires='>=3.0',
)