import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-stackdriver-logging-mdp1",
    version="0.0.8",
    author="Pamela Sanan",
    author_email="pamela.sanan@mavenwave.com",
    description="A module to use for console and stackdriver logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.capella.edu/mdp/mdp_python_logging",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML>=5.3.1',
        'google-cloud-logging>=1.15.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
