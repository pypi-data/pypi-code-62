from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zerocue",
    version="0.3.0",
    packages=find_packages(),

    description="Remove first INDEX track time from every " \
                "following INDEXes in a CUE sheet file",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/shaftoe/zerocue",
    author="Alexander Fortin",

    entry_points={
        "console_scripts": [
            "zerocue = zerocue:main",
        ],
    },

    keywords=[
        "cue",
        "cuesheets",
        "cue-sheets",
        "audio",
    ],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Filters",
        "Topic :: Multimedia :: Sound/Audio",
    ],

    python_requires=">=3.8",

    zip_safe=True,
)
