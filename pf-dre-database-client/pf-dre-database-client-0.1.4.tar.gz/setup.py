from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
long_description = long_description.split('### Development', 1)[0]

setup(
    name="pf-dre-database-client",
    version="0.1.4",
    author="Dominic Hains",
    author_email="d.hains@uq.edu.au",
    description="Provides a client for all Data interactions required with "
                "the Meter Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['mms'],
    install_requires=[
        'psycopg2 >= 2.8.5',
        'pandas',
        'pytz',
        'python-dotenv'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)
