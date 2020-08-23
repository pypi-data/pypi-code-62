"""Setup script."""

from setuptools import setup

package_name = "pbcmd"
description = "PB's miscellaneous command line tools."

with open("README.rst", "r") as fh:
    long_description = fh.read()

classifiers=(
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
)

setup(
    name=package_name,
    description=description,

    author="Parantapa Bhattacharya",
    author_email="pb+pypi@parantapa.net",

    long_description=long_description,
    long_description_content_type="text/x-rst",

    packages=[package_name],
    package_dir={'': 'src'},

    entry_points="""
        [console_scripts]
        pb=pbcmd.cli:cli
    """,

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    install_requires=[
        "click",
        "click_completion",
        "python-dateutil",
        "wasabi",
        "tqdm"
    ],

    url="http://github.com/parantapa/%s" % package_name,
    classifiers=classifiers
)
