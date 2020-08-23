import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotify-client",
    version="1.1.0",
    author="MoodyTunes",
    author_email="moody.tunes.infrastucture@gmail.com",
    description="Client for interacting with the Spotify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moody-Tunes/spotify-client",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.24.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
