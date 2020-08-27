import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordsdk",
    version="0.1.0",
    author="NathaanTFM & DoAltPlusF4",
    author_email="doaltplusf4@gmail.com",
    description="Python wrapper around Discord's Game SDK library.",
    license="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DoAltPlusF4/discord-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
