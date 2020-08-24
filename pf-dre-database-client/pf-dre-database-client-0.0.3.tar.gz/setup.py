from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
long_description = long_description.split('### Set-up', 1)[0]

setup(
    name="pf-dre-database-client",
    version="0.0.3",
    author="Dominic Hains",
    author_email="d.hains@uq.edu.au",
    description="Provides a client for all Data interactions required with "
                "the Meter Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    install_requires=[
        'psycopg2',
        'pandas',
        'pytz'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
