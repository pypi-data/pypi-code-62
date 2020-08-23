import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ytam",
    version="0.0.16",
    author="jayathungek",
    author_email="jayathunge.work@gmail.com",
    description="A commandline utility that enables the creation of albums from Youtube playlists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=["ytam"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['ytam=ytam.cmd:main'],
    },
    install_requires=[
        "certifi",
        "chardet",
        "colorama",
        "idna",
        "mutagen",
        "requests",
        "urllib3"
    ],
    dependency_links=["git+git://github.com/nficano/pytube.git@0f32241c89192b22de9cfbfee1303a1bcee18bd3-0"]
)