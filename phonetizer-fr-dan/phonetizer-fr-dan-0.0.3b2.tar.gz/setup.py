import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phonetizer-fr-dan", # Replace with your own username
    version="0.0.3b2",
    author="Dan Ringwald",
    author_email="dan.ringwald12@gmail.com",
    description="Translates French text to phonetics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biggoron/phonetizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pytest',
        'pandas >= 0.22.0',
        'numpy >= 1.16.0',
        'google-cloud-storage>=1.30.0',
        'pyarrow>=0.15.1',
        'fsspec>=0.8.0',
        'gcsfs==0.6.2'
    ],
    scripts=[
        './scripts/sentence_to_phonem',
        './scripts/phonetizer-test',
        './scripts/phonetizer-train-nn',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=3.6',
    download_url='https://github.com/biggoron/phonetizer/archive/0.0.3b2.tar.gz'
)
