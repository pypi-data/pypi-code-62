import setuptools

with open("README.md", "r") as readme:
    long_description: str = readme.read()

setuptools.setup(
    name="auto_removable_pathlib",
    version="0.0.6",
    author="Alex Konsmanov",
    author_email="alexkoshernosiegov@gmail.com",
    description="The alternative implementation of pathlib.Path's context manager "
                "that automatically removes open file or dir after leaving a 'with ... as' statement",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DobroAlex/auto_removable_pathlib",
    packages=setuptools.find_packages(),
    classifires=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires='>=3.7',
)
