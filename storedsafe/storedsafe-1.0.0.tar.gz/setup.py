import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storedsafe",
    version="1.0.0",
    author="Oscar Mattsson",
    author_email="oscar@storedsafe.com",
    description="Wrapper for the StoredSafe REST-like API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/storedsafe/storedsafe-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
