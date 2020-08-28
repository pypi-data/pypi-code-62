import setuptools
import os

# Convert our Org file into Markdown
os.system("pandoc README.org -t gfm -o README.md")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgg",
    version="0.0.3",
    author="Thiago T. P. Silva",
    author_email="thiagoteodoro501@gmail.com",
    description="Simple Graph Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiagotps/sgg",
    packages=setuptools.find_packages(),
    install_requires = ['matplotlib'],
    keywords="matplotlib graph",
    entry_points={"console_scripts": ["sgg=sgg.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
)
